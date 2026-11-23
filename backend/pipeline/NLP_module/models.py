from dataclasses import dataclass, field
from itertools import count

_entity_ids = count(1)  # in-memory for now; the database will assign IDs later


@dataclass
class TextChunk:
    chunk_id: int
    text: str
    start: int  # character offset in the original text
    end: int


@dataclass
class TextEntity:
    text: str
    source: str = ""
    entity_id: int = field(default_factory=lambda: next(_entity_ids))
    chunks: list[TextChunk] = field(default_factory=list)