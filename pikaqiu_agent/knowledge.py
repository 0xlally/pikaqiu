from __future__ import annotations

import hashlib
import json
import logging
import re
import zipfile
from pathlib import Path
from typing import Iterable

from pikaqiu_agent.storage import MissionStore

logger = logging.getLogger(__name__)


# Domain classification keywords (used to auto-tag knowledge docs)
DOMAIN_KEYWORDS = {
    "ctf_web": [
        "web", "xss", "sqli", "ssrf", "csrf", "jwt", "idor", "cors",
        "graphql", "xxe", "oauth", "file_upload", "template", "403",
        "host-header", "race", "deserialization", "injection", "insecure",
        "upload", "ssti", "lfi", "rfi", "path-traversal", "command-injection",
        "crlf", "open-redirect", "prototype-pollution", "type-juggling",
        "nosql", "ldap-injection", "cve-",
    ],
    "active_directory": [
        "active-directory", "active directory", "kerberos", "bloodhound",
        "ntlm", "dcsync", "adcs", "ldap", "windows-hardening", "domain",
    ],
    "cloud": [
        "cloud", "aws", "azure", "gcp", "iam", "bucket", "s3",
        "kubernetes", "eks", "gke", "lambda", "serverless", "container", "docker",
    ],
    "intranet": [
        "network", "nmap", "smb", "pivot", "tunnel", "reverse-shell",
        "privilege", "linux", "windows", "meterpreter", "psexec", "port-forward",
    ],
}


class KnowledgeIndexer:
    """Indexes knowledge from zip files and directories for RAG retrieval."""

    def __init__(self, workspace_root: Path, store: MissionStore, knowledge_dir: str = "./knowledge") -> None:
        self.workspace_root = workspace_root
        self.store = store
        kb_path = Path(knowledge_dir)
        if not kb_path.is_absolute():
            kb_path = workspace_root / kb_path
        self.kb_root = kb_path
        self.cve_index_path = self.kb_root / "cve-poc-index.json"

    def ensure_ready(self) -> dict[str, int]:
        """Build or verify the knowledge index. Auto-discovers zips and dirs."""
        if not self.kb_root.is_dir():
            return {"status": "no_knowledge_dir"}

        signature = self._build_signature()
        if self.store.get_meta("knowledge_signature") == signature:
            stats = self.store.get_knowledge_stats()
            self._ensure_cve_index()
            return stats

        docs = list(self._iter_docs())
        count = self.store.replace_knowledge_docs(docs)
        self.store.set_meta("knowledge_signature", signature)
        self._ensure_cve_index()
        stats = self.store.get_knowledge_stats()
        stats["rebuilt_docs"] = count
        return stats

    def _ensure_cve_index(self) -> None:
        """Load CVE POC index from JSON if not already loaded."""
        if not self.cve_index_path.exists():
            return
        stat = self.cve_index_path.stat()
        sig = f"{stat.st_mtime_ns}:{stat.st_size}"
        if self.store.get_meta("cve_index_signature") == sig:
            return
        try:
            data = json.loads(self.cve_index_path.read_text(encoding="utf-8"))
            entries = data.get("entries", [])
            count = self.store.replace_cve_index(entries)
            self.store.set_meta("cve_index_signature", sig)
            self.store.set_meta("cve_index_count", str(count))
        except Exception as exc:
            logger.warning("Failed to refresh cve index %s: %s", self.cve_index_path, exc)

    def read_doc_content(self, source: str, path: str, fallback: str = "") -> str:
        """Read a knowledge document by source and path."""
        zip_name, _, inner_path = path.partition(":")
        if zip_name and inner_path:
            zip_path = self.kb_root / zip_name
            if zip_path.exists() and zip_path.suffix == ".zip":
                try:
                    with zipfile.ZipFile(zip_path) as zf:
                        return self._decode_zip_entry(zf.read(inner_path)) or fallback
                except KeyError:
                    return fallback
        # Try as a direct file path relative to kb_root
        direct = self.kb_root / path
        if direct.is_file():
            return self._read_text(direct) or fallback
        return fallback

    def _iter_docs(self) -> Iterable[dict[str, str]]:
        """Iterate over all knowledge documents from zips and directories."""
        seen_hashes: set[str] = set()

        def emit(
            *,
            source: str,
            source_name: str,
            raw_path: str,
            display_path: str,
            title: str,
            dedupe_name: str,
            body: str,
        ) -> Iterable[dict[str, str]]:
            if not body:
                return
            digest = hashlib.sha1(f"{dedupe_name}\n{body}".encode("utf-8", "ignore")).hexdigest()
            if digest in seen_hashes:
                return
            seen_hashes.add(digest)
            compact_body = re.sub(r"\n{4,}", "\n\n\n", re.sub(r"\r\n?", "\n", body)).strip()[:24000]
            for domain in self._domains_from_path(raw_path, source_name):
                yield {
                    "source": source,
                    "domain": domain,
                    "title": title,
                    "path": display_path,
                    "body": compact_body,
                }

        for source_dir in sorted(item for item in self.kb_root.iterdir() if item.is_dir()):
            for md_file in sorted(source_dir.rglob("*.md")):
                rel_path = md_file.relative_to(self.kb_root).as_posix()
                yield from emit(
                    source=source_dir.name,
                    source_name=source_dir.name,
                    raw_path=rel_path,
                    display_path=rel_path,
                    title=md_file.stem.replace("-", " ").title(),
                    dedupe_name=md_file.name,
                    body=self._read_text(md_file),
                )

        for zip_path in sorted(self.kb_root.glob("*.zip")):
            with zipfile.ZipFile(zip_path) as zf:
                for info in zf.infolist():
                    lowered = info.filename.lower()
                    if info.is_dir() or not lowered.endswith((".md", ".rst")) or "/banners/" in lowered:
                        continue
                    yield from emit(
                        source=zip_path.name,
                        source_name=zip_path.stem,
                        raw_path=info.filename,
                        display_path=f"{zip_path.name}:{info.filename}",
                        title=Path(info.filename).name,
                        dedupe_name=Path(info.filename).name,
                        body=self._decode_zip_entry(zf.read(info)),
                    )

    def _build_signature(self) -> str:
        """Build a hash signature of all knowledge sources for cache invalidation."""
        parts: list[str] = []
        for item in sorted(self.kb_root.iterdir()):
            if item.is_file() and item.suffix == ".zip":
                stat = item.stat()
                parts.append(f"{item.name}:{stat.st_mtime_ns}:{stat.st_size}")
            elif item.is_dir():
                markers = []
                for file_path in sorted(item.rglob("*.md")):
                    stat = file_path.stat()
                    rel = file_path.relative_to(item).as_posix()
                    markers.append(f"{rel}:{stat.st_mtime_ns}:{stat.st_size}")
                digest = hashlib.sha1("|".join(markers).encode("utf-8")).hexdigest()
                parts.append(f"{item.name}:{digest}")
        return hashlib.sha1("||".join(parts).encode("utf-8")).hexdigest()

    def _read_text(self, path: Path) -> str:
        if not path.exists():
            return ""
        for encoding in ("utf-8", "utf-8-sig", "gb18030"):
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        return path.read_text(encoding="utf-8", errors="replace")

    def _decode_zip_entry(self, data: bytes) -> str:
        for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
            try:
                return data.decode(encoding).strip()
            except UnicodeDecodeError:
                continue
        return data.decode("utf-8", "replace").strip()

    def _domains_from_path(self, raw_path: str, source_name: str) -> list[str]:
        """Classify a document into domains based on path keywords."""
        lowered = raw_path.lower().replace("\\", "/")
        domains = [
            domain
            for domain, keywords in DOMAIN_KEYWORDS.items()
            if any(keyword in lowered for keyword in keywords)
        ]
        if not domains:
            # Default domain based on source name
            source_lower = source_name.lower()
            if "howtohunt" in source_lower or "payloadsallthethings" in source_lower:
                domains.append("ctf_web")
            elif "hacktricks" in source_lower:
                domains.append("intranet")
            else:
                domains.append("ctf_web")
        return domains
