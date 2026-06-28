from __future__ import annotations

import hashlib
import importlib
import logging
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any, Iterable

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
    """Indexes knowledge files and exposes a project-local RAG search API."""

    def __init__(self, workspace_root: Path, store: MissionStore, knowledge_dir: str = "./knowledge") -> None:
        self.workspace_root = workspace_root
        self.store = store
        kb_path = Path(knowledge_dir)
        if not kb_path.is_absolute():
            kb_path = workspace_root / kb_path
        self.kb_root = kb_path.resolve()
        self._rag_dir = self.workspace_root / "rag"
        self._rag_index_dir = self._rag_dir / "faiss_db"
        self._rag_client: Any | None = None
        self._rag_error = ""

    def ensure_ready(self) -> dict[str, Any]:
        """Build or verify the knowledge index and the optional RAG index."""
        if not self.kb_root.is_dir():
            return {"status": "no_knowledge_dir", **self._rag_snapshot()}

        signature = self._build_signature()
        rebuilt_docs = 0
        if self.store.get_meta("knowledge_signature") != signature:
            docs = list(self._iter_docs())
            rebuilt_docs = self.store.replace_knowledge_docs(docs)
            self.store.set_meta("knowledge_signature", signature)

        self._ensure_rag_ready(signature)

        stats = self.get_stats()
        if rebuilt_docs:
            stats["rebuilt_docs"] = rebuilt_docs
        return stats

    def get_stats(self) -> dict[str, Any]:
        stats = self.store.get_knowledge_stats()
        stats["search_backend"] = "rag" if self._rag_is_available() else "fts"
        stats["rag"] = self._rag_snapshot()
        return stats

    def search(
        self,
        query: str,
        domains: list[str] | None = None,
        limit: int = 6,
    ) -> list[dict[str, Any]]:
        query = query.strip()
        if not query:
            return []

        limit = max(1, min(int(limit), 50))
        candidate_limit = max(limit * 8, 24)
        expanded_query = self._expand_search_query(query)

        candidates: list[dict[str, Any]] = []
        candidates.extend(self._search_with_rag(query, domains=domains, limit=candidate_limit))
        candidates.extend(self.store.search_knowledge(query, domains=domains, limit=candidate_limit))
        if expanded_query != query:
            candidates.extend(self.store.search_knowledge(expanded_query, domains=domains, limit=candidate_limit))

        ranked = self._rank_and_trim_results(query, candidates, limit=limit)
        if ranked:
            return ranked
        return self.store.search_knowledge(query, domains=domains, limit=limit)

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

        direct = self.kb_root / path
        if direct.is_file():
            return self._read_text(direct) or fallback
        return fallback

    def _ensure_rag_ready(self, signature: str) -> None:
        if not self._rag_dir.is_dir():
            self._rag_error = "rag directory not found"
            self._rag_client = None
            return

        if not self._rag_modules_available():
            return

        rag_sig = self.store.get_meta("knowledge_rag_signature")
        if rag_sig != signature or not self._rag_index_files_exist():
            if not self._build_rag_index():
                self._rag_client = None
                return
            self.store.set_meta("knowledge_rag_signature", signature)
            self._load_rag_client(force_reload=True)
            return

        if not self._rag_is_available():
            self._load_rag_client(force_reload=False)

    def _rag_modules_available(self) -> bool:
        try:
            importlib.import_module("rag.rag_client")
            return True
        except Exception as exc:
            self._rag_error = str(exc)
            logger.warning("RAG client import failed: %s", exc)
            return False

    def _build_rag_index(self) -> bool:
        script_path = self._rag_dir / "rag_kdprepare.py"
        if not script_path.is_file():
            self._rag_error = f"missing builder: {script_path}"
            return False

        env = os.environ.copy()
        env["PIKAQIU_RAG_KNOWLEDGE_DIR"] = str(self.kb_root)
        cmd = [sys.executable, str(script_path)]
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(self.workspace_root),
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=3600,
            )
        except Exception as exc:
            self._rag_error = str(exc)
            logger.warning("RAG index build failed to start: %s", exc)
            return False

        combined = "\n".join(part.strip() for part in (proc.stdout, proc.stderr) if part.strip())
        if proc.returncode != 0:
            self._rag_error = combined or f"rag_kdprepare exit code {proc.returncode}"
            logger.warning("RAG index build failed: %s", self._rag_error)
            return False

        self._rag_error = ""
        if combined:
            logger.info("RAG index build output:\n%s", combined)
        return True

    def _load_rag_client(self, *, force_reload: bool) -> None:
        try:
            module = importlib.import_module("rag.rag_client")
            if force_reload and hasattr(module, "_rag_client_instance"):
                module._rag_client_instance = None
            client = module.get_rag_client(str(self.workspace_root))
            if client is None or not client.is_available() or client.index is None:
                self._rag_client = None
                self._rag_error = "rag client unavailable or index missing"
                return
            self._rag_client = client
            self._rag_error = ""
        except Exception as exc:
            self._rag_client = None
            self._rag_error = str(exc)
            logger.warning("Failed to load RAG client: %s", exc)

    def _rag_index_files_exist(self) -> bool:
        return (
            (self._rag_index_dir / "kb.faiss").is_file()
            and (self._rag_index_dir / "kb_store.json").is_file()
        )

    def _rag_is_available(self) -> bool:
        return bool(
            self._rag_client is not None
            and getattr(self._rag_client, "index", None) is not None
            and self._rag_client.is_available()
        )

    def _search_with_rag(
        self,
        query: str,
        *,
        domains: list[str] | None,
        limit: int,
    ) -> list[dict[str, Any]]:
        if not self._rag_is_available():
            return []

        fetch_limit = max(limit * 4, 12)
        try:
            raw_results = self._rag_client.query(query, top_k=fetch_limit)
        except Exception as exc:
            self._rag_error = str(exc)
            logger.warning("RAG query failed, falling back to FTS: %s", exc)
            return []

        items: list[dict[str, Any]] = []
        seen_paths: set[str] = set()
        for row in raw_results:
            rel_path = self._normalize_rag_path(row)
            if not rel_path:
                continue
            if rel_path.lower().endswith("/summary.md"):
                continue
            if rel_path in seen_paths:
                continue

            source = self._source_from_path(rel_path)
            row_domains = self._domains_from_path(rel_path, source)
            if domains and not any(domain in row_domains for domain in domains):
                continue

            snippet = str(row.get("snippet") or "").strip()
            if not snippet:
                continue

            doc_id = self.store.find_knowledge_doc_id(source=source, path=rel_path)
            items.append(
                {
                    "id": doc_id,
                    "source": source,
                    "domain": row_domains[0] if row_domains else "ctf_web",
                    "domains": row_domains,
                    "title": self._rag_title(rel_path),
                    "path": rel_path,
                    "snippet": snippet,
                    "body": snippet,
                    "score": float(row.get("score", 0.0)),
                }
            )
            seen_paths.add(rel_path)
            if len(items) >= limit:
                break

        return items

    def _rank_and_trim_results(
        self,
        query: str,
        candidates: list[dict[str, Any]],
        *,
        limit: int,
    ) -> list[dict[str, Any]]:
        terms = self._query_terms(query)
        if not terms:
            return candidates[:limit]

        best_by_path: dict[str, tuple[float, dict[str, Any]]] = {}
        for item in candidates:
            path = str(item.get("path") or "").replace("\\", "/")
            if not path:
                continue
            full_text = self.read_doc_content(
                str(item.get("source") or ""),
                path,
                fallback=str(item.get("body") or item.get("snippet") or ""),
            )
            score = self._result_score(query, terms, item, full_text)
            if score <= 0:
                continue

            ranked_item = dict(item)
            snippet = self._anchored_snippet(
                full_text or str(item.get("body") or ""),
                terms,
                query=query,
            )
            if snippet:
                ranked_item["snippet"] = snippet
                ranked_item["body"] = snippet
            ranked_item["score"] = score

            current = best_by_path.get(path)
            if current is None or score > current[0]:
                best_by_path[path] = (score, ranked_item)

        ranked = sorted(best_by_path.values(), key=lambda row: row[0], reverse=True)
        if not ranked:
            return []

        top_score = ranked[0][0]
        threshold = max(2.0, top_score * 0.18)
        filtered = [item for score, item in ranked if score >= threshold]
        return filtered[:limit]

    def _result_score(
        self,
        query: str,
        terms: list[str],
        item: dict[str, Any],
        full_text: str,
    ) -> float:
        title = str(item.get("title") or "")
        path = str(item.get("path") or "")
        source = str(item.get("source") or "")
        snippet = str(item.get("snippet") or item.get("body") or "")
        haystack = self._searchable_text(f"{title}\n{path}\n{full_text or snippet}")
        title_path = self._searchable_text(f"{title}\n{path}")

        score = min(float(item.get("score") or 0.0), 3.0) * 0.25
        coverage = 0
        strong_hits = 0
        for term in terms:
            if len(term) < 2:
                continue
            normalized = self._searchable_text(term)
            if not normalized:
                continue
            if normalized in title_path:
                score += 3.0 if self._is_strong_term(normalized) else 1.5
                coverage += 1
                strong_hits += 1 if self._is_strong_term(normalized) else 0
            elif normalized in haystack:
                score += 1.6 if self._is_strong_term(normalized) else 0.7
                coverage += 1
                strong_hits += 1 if self._is_strong_term(normalized) else 0

        lowered_query = query.lower()
        lowered_path = path.lower()
        lowered_source = source.lower()
        if "request smuggling" in lowered_query and "request-smuggling" in lowered_path:
            score += 5.0
        wants_payload = any(token in lowered_query for token in ("payload", "poc", "exploit"))
        if wants_payload:
            if lowered_source == "payloadsallthethings":
                score += 7.0
            if self._looks_like_payload(full_text or snippet):
                score += 2.5
            if any(part in lowered_path for part in ("/lab-", "/finding", "/exploiting", "request smuggling/readme")):
                score += 3.0
            if any(part in lowered_path for part in ("/blog/", "/research/")):
                score -= 1.5
        if lowered_source == "portswigger":
            score += 0.8
        elif lowered_source == "payloadsallthethings":
            score += 0.8

        score += min(coverage, 8) * 0.4
        score += min(strong_hits, 5) * 0.8

        core_terms = [t for t in terms if self._is_strong_term(self._searchable_text(t))]
        if core_terms and strong_hits == 0:
            score *= 0.35
        if self._is_noise_for_query(query, item, haystack):
            score *= 0.15
        return score

    @staticmethod
    def _is_strong_term(term: str) -> bool:
        if len(term) >= 4:
            return True
        return term in {"cl.te", "te.cl", "h2.cl", "h2.te", "cl.0", "0.cl"}

    @staticmethod
    def _looks_like_payload(text: str) -> bool:
        lowered = (text or "").lower()
        indicators = [
            "content-length:",
            "transfer-encoding:",
            "http/1.1",
            "post /",
            "get /",
            "\\r\\n",
            "chunked",
            "payload",
        ]
        return sum(1 for indicator in indicators if indicator in lowered) >= 2

    @staticmethod
    def _is_noise_for_query(query: str, item: dict[str, Any], haystack: str) -> bool:
        lowered_query = query.lower()
        source = str(item.get("source") or "").lower()
        path = str(item.get("path") or "").lower()
        if "request smuggling" in lowered_query:
            if "request smuggling" not in haystack and "request-smuggling" not in path:
                return True
            if source == "gtfobins.github.io":
                return True
        return False

    def _anchored_snippet(
        self,
        text: str,
        terms: list[str],
        *,
        max_len: int = 1400,
        query: str = "",
    ) -> str:
        content = re.sub(r"\r\n?", "\n", text or "").strip()
        if not content:
            return ""
        searchable = self._searchable_text(content)
        if len(content) <= max_len:
            return content

        best_idx = -1
        best_score = -1.0
        for term in terms:
            normalized = self._searchable_text(term)
            if not normalized:
                continue
            start = 0
            while True:
                idx = searchable.find(normalized, start)
                if idx < 0:
                    break
                window = searchable[max(0, idx - 300): idx + 300]
                local_score = sum(1 for t in terms if self._searchable_text(t) in window)
                if self._is_strong_term(normalized):
                    local_score += 3
                if any(token in query.lower() for token in ("payload", "poc", "exploit")):
                    local_score += sum(
                        2
                        for indicator in (
                            "content-length:",
                            "transfer-encoding:",
                            "http/1.1",
                            "post /",
                            "get /",
                        )
                        if indicator in window
                    )
                if local_score > best_score:
                    best_score = float(local_score)
                    best_idx = idx
                start = idx + max(len(normalized), 1)

        if best_idx < 0:
            return content[:max_len].rstrip() + "..."

        start = max(0, best_idx - max_len // 3)
        end = min(len(content), start + max_len)
        start = max(0, content.rfind("\n\n", 0, start) + 2) if start else 0
        end_boundary = content.find("\n\n", end)
        if 0 <= end_boundary <= end + 240:
            end = end_boundary
        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet += "..."
        return snippet

    def _expand_search_query(self, query: str) -> str:
        terms = self._query_terms(query)
        return " ".join(dict.fromkeys([query, *terms]))

    @classmethod
    def _query_terms(cls, query: str) -> list[str]:
        raw_terms = [
            token.lower()
            for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_./:+-]*|[\u4e00-\u9fff]{2,}", query or "")
        ]
        terms: list[str] = []
        terms.extend(raw_terms)
        terms.extend(cls._security_pair_variants(raw_terms))

        lowered = " ".join(raw_terms)
        for phrase in (
            "request smuggling",
            "content length",
            "transfer encoding",
            "server side template injection",
            "server side request forgery",
        ):
            if phrase in lowered:
                terms.append(phrase)
                terms.append(phrase.replace(" ", "-"))

        return [term for term in dict.fromkeys(terms) if len(term) >= 2]

    @staticmethod
    def _security_pair_variants(tokens: list[str]) -> list[str]:
        variants: list[str] = []
        short = {"cl", "te", "h2", "h1", "0"}
        for first, second in zip(tokens, tokens[1:]):
            if first in short and second in short:
                variants.extend(
                    [
                        f"{first}.{second}",
                        f"{first}-{second}",
                        f"{first}_{second}",
                        f"{first}{second}",
                    ]
                )
        return variants

    @staticmethod
    def _searchable_text(value: str) -> str:
        lowered = (value or "").lower()
        lowered = lowered.replace("_", ".").replace("-", ".")
        lowered = re.sub(r"\s+", " ", lowered)
        lowered = re.sub(r"\b(content)\s+(length)\b", r"\1-\2", lowered)
        lowered = re.sub(r"\b(transfer)\s+(encoding)\b", r"\1-\2", lowered)
        return lowered

    def _normalize_rag_path(self, row: dict[str, Any]) -> str:
        doc_id = str(row.get("doc_id") or "").strip()
        if doc_id:
            return self._normalize_relative_path(doc_id)

        doc_meta = row.get("meta", {}).get("doc_meta", {})
        raw_path = str(doc_meta.get("path") or "").strip()
        if not raw_path:
            return ""
        return self._normalize_relative_path(raw_path)

    def _normalize_relative_path(self, raw_path: str) -> str:
        value = raw_path.replace("\\", "/").strip()
        if not value:
            return ""

        try:
            path_obj = Path(value)
            if path_obj.is_absolute():
                return path_obj.relative_to(self.kb_root).as_posix()
        except Exception:
            pass

        kb_name = self.kb_root.name + "/"
        if value.startswith(kb_name):
            return value[len(kb_name):]
        return value

    def _source_from_path(self, rel_path: str) -> str:
        parts = Path(rel_path).parts
        return parts[0] if parts else "rag"

    def _rag_title(self, rel_path: str) -> str:
        stem = Path(rel_path).stem.replace("-", " ").replace("_", " ").strip()
        return stem.title() if stem else rel_path

    def _rag_snapshot(self) -> dict[str, Any]:
        total_chunks = 0
        if self._rag_is_available():
            total_chunks = int(getattr(self._rag_client.index, "ntotal", 0))
        return {
            "available": self._rag_is_available(),
            "total_chunks": total_chunks,
            "error": self._rag_error,
        }

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
            for doc_file in sorted(
                path for path in source_dir.rglob("*")
                if path.is_file() and path.suffix.lower() in {".md", ".txt"}
            ):
                rel_path = doc_file.relative_to(self.kb_root).as_posix()
                yield from emit(
                    source=source_dir.name,
                    source_name=source_dir.name,
                    raw_path=rel_path,
                    display_path=rel_path,
                    title=doc_file.stem.replace("-", " ").replace("_", " ").title(),
                    dedupe_name=doc_file.name,
                    body=self._read_text(doc_file),
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
                for file_path in sorted(
                    path for path in item.rglob("*")
                    if path.is_file() and path.suffix.lower() in {".md", ".txt"}
                ):
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
            source_lower = source_name.lower()
            if "howtohunt" in source_lower or "payloadsallthethings" in source_lower:
                domains.append("ctf_web")
            elif "hacktricks" in source_lower:
                domains.append("intranet")
            else:
                domains.append("ctf_web")
        return domains
