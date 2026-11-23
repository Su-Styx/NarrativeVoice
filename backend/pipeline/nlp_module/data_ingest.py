# this file will read and ingest data, call from chunking.py and return the chunked data to engine

from pathlib import Path

from .chunking import chunk_data
from .models import TextEntity

# max characters per chunk (roughly 4 chars per token). Keep well under the
# model's context window, since the prompt and the output also need room.
CHUNK_CHARS = {"qwen3:14b": 3000, "qwen3:1.7b": 1200}
DEFAULT_MODEL = "qwen3:14b"


def read_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
    return path.read_text(encoding="utf-8")


def data_ingest(file_path, model_name: str = DEFAULT_MODEL) -> TextEntity:
    path = Path(file_path)
    text = read_file(path)
    if not text.strip():
        raise ValueError(f"No text could be read from {path}")

    entity = TextEntity(text=text, source=str(path))
    entity.chunks = chunk_data(text, CHUNK_CHARS[model_name])
    return entity