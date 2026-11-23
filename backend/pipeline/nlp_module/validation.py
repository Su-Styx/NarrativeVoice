import re
import unicodedata

from models import InterviewExtraction

BANNED_STARTS = ("themes are", "challenges are", "experiences are",
                 "topics are", "stated links are")
MIN_QUOTE, MAX_QUOTE = 5, 300


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def _punct(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    for a, b in {"’": "'", "‘": "'", "“": '"', "”": '"', "—": "-", "–": "-"}.items():
        s = s.replace(a, b)
    return s


def diagnose(quote: str, source: str) -> str:
    if quote in _ws(source):
        return "whitespace"
    q, s = _ws(_punct(quote)), _ws(_punct(source))
    if q in s:
        return "unicode_or_punctuation"
    if q.lower() in s.lower():
        return "case"
    return "paraphrased_or_fabricated"


def check_item(item, source_text: str, expected_chunk_id: str) -> list[dict]:
    base = {"field": item.field, "quote": item.exact_quote}
    problems = []
    q = item.exact_quote

    if item.source_chunk_id != expected_chunk_id:
        problems.append({**base, "type": "source_chunk_id_mismatch",
                         "expected": expected_chunk_id,
                         "received": item.source_chunk_id})

    if not item.statement.strip():
        problems.append({**base, "type": "empty_statement"})
    elif item.statement.lower().startswith(BANNED_STARTS):
        problems.append({**base, "type": "generic_statement"})

    if "..." in q or "…" in q:
        problems.append({**base, "type": "non_contiguous_quote"})
    elif not MIN_QUOTE <= len(q) <= MAX_QUOTE:
        problems.append({**base, "type": "quote_length"})
    elif q not in source_text:
        problems.append({**base, "type": "quote_not_found",
                         "diagnosis": diagnose(q, source_text)})
    return problems


def validate_extraction(extraction: dict, source_text: str,
                        expected_chunk_id: str) -> dict:
    if extraction["parsed"] is None:
        return {
            "schema_valid": False, "quotes_checked": 0, "quotes_verified": 0,
            "quote_success_rate": 0.0, "all_quotes_verified": False,
            "failures": [{"type": "schema_invalid",
                          "detail": extraction["schema_error"]}],
            "failures_by_field": {}, "failure_types": {"schema_invalid": 1},
            "diagnoses": {}, "quote_reuse": {}, "accepted": [],
        }

    parsed = InterviewExtraction.model_validate(extraction["parsed"])
    failures, accepted, reuse = [], [], {}

    for item in parsed.evidence:
        reuse[item.exact_quote] = reuse.get(item.exact_quote, 0) + 1
        problems = check_item(item, source_text, expected_chunk_id)
        if problems:
            failures.extend(problems)
        else:
            accepted.append(item.model_dump())

    checked = len(parsed.evidence)
    verified = len(accepted)

    def tally(key):
        out = {}
        for f in failures:
            if key in f:
                out[f[key]] = out.get(f[key], 0) + 1
        return out

    return {
        "schema_valid": True,
        "quotes_checked": checked,
        "quotes_verified": verified,
        "quote_success_rate": verified / checked if checked else 0.0,
        "all_quotes_verified": checked > 0 and not failures,
        "failures": failures,
        "failures_by_field": tally("field"),
        "failure_types": tally("type"),
        "diagnoses": tally("diagnosis"),
        "quote_reuse": {q: n for q, n in reuse.items() if n > 2},
        "accepted": accepted,
    }