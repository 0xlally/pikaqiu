from __future__ import annotations

import logging
import os
import threading
from typing import Any

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

_global_model: Any | None = None
_model_lock = threading.Lock()


def get_embedding_model(project_root: str | None = None) -> Any | None:
    """Return a shared embedding model instance when available."""
    global _global_model

    if _global_model is not None:
        return _global_model

    with _model_lock:
        if _global_model is not None:
            return _global_model

        if SentenceTransformer is None:
            logger.info("sentence-transformers unavailable; using hash embeddings")
            return None

        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        local_model_path = os.path.join(project_root, "rag", "models", "all-MiniLM-L6-v2")
        model_config_path = os.path.join(local_model_path, "config.json")

        if os.path.exists(model_config_path):
            try:
                _global_model = SentenceTransformer(local_model_path)
                logger.info("Loaded local embedding model from %s", local_model_path)
                return _global_model
            except Exception as exc:
                logger.warning("Failed to load local embedding model: %s", exc)

        try:
            _global_model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
            logger.info("Loaded cached embedding model all-MiniLM-L6-v2")
            return _global_model
        except Exception as exc:
            logger.info("Embedding model unavailable, falling back to hash embeddings: %s", exc)
            return None


def get_model_dim(model: Any | None = None, default_dim: int = 384) -> int:
    if model is None:
        model = _global_model
    if model is None:
        return default_dim
    try:
        return int(getattr(model, "get_sentence_embedding_dimension", lambda: default_dim)())
    except Exception:
        return default_dim
