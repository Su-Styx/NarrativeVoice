from pathlib import Path

import yaml


def load_profile(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        profile = yaml.safe_load(file)

    if not profile or "profile" not in profile:
        raise ValueError(f"Invalid profile file: {path}")

    return profile


def build_system_prompt(profile: dict) -> str:
    instructions = "\n".join(
        f"- {instruction}"
        for instruction in profile["instructions"]
    )

    fields = "\n".join(
        f"- {name}: {spec.get('description', '')}".strip()
        for name, spec in profile["fields"].items()
    )

    return f"""You are a careful technical-document extraction assistant.

TASK
{profile['description']}

AVAILABLE FIELDS
{fields}

RULES
{instructions}

Return only JSON that conforms to the supplied JSON schema.
"""


def build_user_prompt(chunk: dict) -> str:
    return f"""DOCUMENT TEXT:
{chunk['text']}

SOURCE CHUNK ID:
{chunk['chunk_id']}
"""