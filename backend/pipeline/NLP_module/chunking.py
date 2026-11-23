# file here will chunk the ingested data
# note that chunking will depend on the model, focus on the sweetspot for the model's token limit



import re

from .models import TextChunk


def chunk_data(text: str, max_chars: int) -> list[TextChunk]:
    """Pack consecutive lines (speaker turns) into chunks up to max_chars.
    Never cuts inside a line; a single line longer than max_chars stays whole."""
    chunks: list[TextChunk] = []
    start = end = None

    for m in re.finditer(r"[^\n]+", text):
        if start is None:
            start, end = m.start(), m.end()
        elif m.end() - start > max_chars:
            chunks.append(TextChunk(len(chunks), text[start:end], start, end))
            start, end = m.start(), m.end()
        else:
            end = m.end()

    if start is not None:
        chunks.append(TextChunk(len(chunks), text[start:end], start, end))
    return chunks