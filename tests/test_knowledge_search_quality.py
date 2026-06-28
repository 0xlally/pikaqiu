from pathlib import Path

from pikaqiu_agent.knowledge import KnowledgeIndexer
from pikaqiu_agent.storage import MissionStore


class DummyRagClient:
    index = object()

    def is_available(self):
        return True

    def query(self, text, top_k=10):
        return [
            {
                "doc_id": "PortSwigger/web-security/request-smuggling.md",
                "score": 1.85,
                "snippet": "HTTP request smuggling overview.",
            },
            {
                "doc_id": "GTFOBins.github.io/index.md",
                "score": 1.4,
                "snippet": "GTFOBins is a list of Unix binaries.",
            },
        ]


def write_doc(root: Path, rel_path: str, body: str) -> None:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_request_smuggling_query_prefers_specific_payload_docs(tmp_path):
    kb = tmp_path / "knowledge"
    write_doc(
        kb,
        "PortSwigger/web-security/request-smuggling.md",
        "# HTTP request smuggling\n\nGeneral overview of request smuggling.",
    )
    write_doc(
        kb,
        "PortSwigger/web-security/request-smuggling/finding.md",
        """# Finding HTTP request smuggling vulnerabilities

Finding CL.TE vulnerabilities using timing techniques.

POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Content-Length: 4

1
A
X
""",
    )
    write_doc(
        kb,
        "PayloadsAllTheThings/Request Smuggling/README.md",
        """# Request Smuggling

CL.TE payload:

POST / HTTP/1.1
Host: example.com
Content-Length: 6
Transfer-Encoding: chunked
""",
    )
    write_doc(
        kb,
        "GTFOBins.github.io/index.md",
        "# GTFOBins\n\nThis is not a request smuggling reference.",
    )

    store = MissionStore(":memory:")
    idx = KnowledgeIndexer(tmp_path, store, "./knowledge")
    idx.ensure_ready()
    idx._rag_client = DummyRagClient()

    results = idx.search("HTTP request smuggling CL TE desync payload", limit=3)

    paths = [item["path"] for item in results]
    assert "GTFOBins.github.io/index.md" not in paths
    assert paths[0] in {
        "PortSwigger/web-security/request-smuggling/finding.md",
        "PayloadsAllTheThings/Request Smuggling/README.md",
    }
    assert "Transfer-Encoding" in results[0]["snippet"]
