import time
from typing import Any

from ollama import chat
from pydantic import BaseModel
from pydantic import ValidationError
from models import InterviewExtraction
from prompts import build_system_prompt, build_user_prompt


def extract_from_chunk(
    profile: dict,
    chunk: dict,
    model_tag: str | None = None,
) -> dict[str, Any]:
    model = model_tag or profile["model"]["default"]
    options = {
        "temperature": profile["model"]["temperature"],
        "num_ctx": profile["model"]["num_ctx"],
    }

    messages = [
        {"role": "system", "content": build_system_prompt(profile)},
        {"role": "user", "content": build_user_prompt(chunk)},
    ]

    started = time.perf_counter()
    response = chat(
        model=model,
        messages=messages,
        format=InterviewExtraction.model_json_schema(),
        options=options,
    )
    elapsed_ms = int((time.perf_counter() - started) * 1000)


    raw_response = response.message.content

    try:
        parsed = InterviewExtraction.model_validate_json(raw_response).model_dump()
        schema_error = None
    except ValidationError as exc:
        parsed = None
        schema_error = str(exc)

    return {
        "document_id": chunk["document_id"],
        "chunk_id": chunk["chunk_id"],
        "model_tag": model,
        "profile": profile["profile"],
        "profile_version": profile["version"],
        "options": options,
        "raw_response": raw_response,
        "parsed": parsed,
        "schema_error": schema_error,
        "elapsed_ms": elapsed_ms,
    }