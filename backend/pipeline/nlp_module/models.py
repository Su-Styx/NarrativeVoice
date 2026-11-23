from typing import Literal
from pydantic import BaseModel, Field, field_validator


# ALLOWED_FIELDS = {
#     "themes",
#     "challenges",
#     "experiences",
#     "topics",
#     "stated_links",
# }




class EvidenceItem(BaseModel):
    field: Literal["themes", "challenges", "experiences", "topics", "stated_links"]
    statement: str
    exact_quote: str
    source_chunk_id: str


class InterviewExtraction(BaseModel):
    summary: str
    evidence: list[EvidenceItem] = Field(default_factory=list)