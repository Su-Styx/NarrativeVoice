# file here will chunk the ingested data
# note that chunking will depend on the model, focus on the sweetspot for the model's token limit

import argparse
import json
from pathlib import Path

from pypdf import PdfReader
import re, unicodedata


import re, unicodedata

def clean_text(t: str) -> str:
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("\r", "").replace("\xa0", " ")
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"(\w)-\n(\w)", r"\1-\2", t)   # rejoin line-end hyphenation
    t = re.sub(r"\s+", " ", t)                # every run of whitespace -> one space
    t = t.replace("\r", "") #removed carriage returns
    return t.strip()

def chunk_sentences(text: str, max_chars: int = 1200) -> list[str]:
    sentences = re.split(r"(?<=[.!?]) (?=[A-Z\"'])", text)
    chunks, cur = [], ""
    for s in sentences:
        if cur and len(cur) + 1 + len(s) > max_chars:
            chunks.append(cur)
            cur = s
        else:
            cur = f"{cur} {s}".strip()
    if cur:
        chunks.append(cur)
    return chunks

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--pages", required=True)
    parser.add_argument("--chunk-size", type=int, default=1200)
    args = parser.parse_args()

    reader = PdfReader(args.pdf)
    page_numbers = []

    

    for part in args.pages.split(","):
        if "-" in part:
            start, end = part.split("-")
            page_numbers.extend(range(int(start), int(end) + 1))
        else:
            page_numbers.append(int(part))

    text_parts = []

    for page_number in page_numbers:
        page = reader.pages[page_number - 1]
        text_parts.append(page.extract_text() or "")
    

    full_text = "\n\n".join(text_parts).strip()

    if not full_text:
        raise SystemExit("No extractable text found in the selected pages.")
    
    # full_text = clean_text(full_text) 

    full_text = clean_text(" ".join(text_parts))
    chunk_texts = chunk_sentences(full_text, args.chunk_size)

    chunks = []
    chunk_index = 1

    for start in range(0, len(full_text), args.chunk_size):
        chunk_text = full_text[start:start + args.chunk_size].strip()

        if not chunk_text:
            continue

        chunks.append(
            {
                "chunk_id": f"{args.document_id}:chunk_{chunk_index:02d}",
                "text": chunk_text,
            }
        )
        chunk_index += 1

    payload = {
        "documents": [
            {
                "document_id": args.document_id,
                "title": args.title,
                "source_type": "real_document_excerpt",
                "source_file": str(Path(args.pdf).name),
                "source_pages": args.pages,
                "chunks": chunks,
            }
        ]
    }

    with open(args.output, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    print(f"Wrote {len(chunks)} chunks to {args.output}")


if __name__ == "__main__":
    main()

