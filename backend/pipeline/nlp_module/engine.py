# primary working file for running and testing the NLP module

# the engine is called to begin task, calls data_ingest to read and ingest data -> chunked
# data_ingest.py returns data to engine.py, which calls the prompts.py file to generate the prompt
# prompt is then passed onto ollama for processing, response is returned to engine.py


# 1. data is chunked 
# 2. data is passed to prompt gen. 
# 3. each chunk + prompt is serially passed to ollama for processing
# 3.a. pydantic verifies outputted result accurately matches schema and flags any innacurate results
# 3.b. chunks with paraphrasing/ no sub-string match/evidence will be re-attempted (max 2 attempts) with a new prompt to ensure accuracy of results
# 4. result of each chunk + prompt is stored, then combined into a single JSON file
# 5. the master-JSON file is read by the engine upon completion and cross-chunk analysis may begin

# import sys
# from pathlib import Path

# from .data_ingest import data_ingest

# DEFAULT_PATH = Path(__file__).parent / "data_repo" / "Hamlet-PDF.txt"


# def main():
#     path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH

#     # section 0 - data ingestion
#     entity = data_ingest(path)
#     print(f"entity {entity.entity_id}: {len(entity.text)} chars, {len(entity.chunks)} chunks")
#     for c in entity.chunks:
#         print(f"  chunk {c.chunk_id} [{c.start}:{c.end}] {c.text[:60]!r}")

#     print("finished executing")


# if __name__ == "__main__":
#     main()

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from models import InterviewExtraction

from extraction import extract_from_chunk
from prompts import load_profile
from validation import validate_extraction


def load_documents(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as file:
        payload = json.load(file)

    documents = payload["documents"]
    chunks = []

    for document in documents:
        for chunk in document["chunks"]:
            chunks.append(
                {
                    "document_id": document["document_id"],
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                }
            )

    return chunks



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["extract"])
    parser.add_argument("--profile", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--output-dir", default="runs")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    chunks = load_documents(args.input)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for chunk in chunks:
        print(f"Extracting {chunk['chunk_id']}...")

        extraction = extract_from_chunk(
            profile=profile,
            chunk=chunk,
            model_tag=args.model,
        )

        validation = validate_extraction(
            extraction=extraction,
            source_text=chunk["text"],
            expected_chunk_id=chunk["chunk_id"],
        )

        record = {
            **extraction,
            "validation": validation,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        output_path = output_dir / f"{chunk['chunk_id'].replace(':', '__')}.json"

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(record, file, indent=2, ensure_ascii=False)

        status = "PASS" if validation["all_quotes_verified"] else "FAIL"
        print(f"{status}: {output_path}")

        if not validation["all_quotes_verified"]:
            print(json.dumps(validation["failures"], indent=2))




if __name__ == "__main__":
    main()

























# old main file: 
# import argparse
# import json
# from datetime import datetime, timezone
# from pathlib import Path




# def load_documents(path: str) -> list[dict]:
#     with open(path, "r", encoding="utf-8") as file:
#         payload = json.load(file)

#     documents = payload["documents"]
#     chunks = []

#     for document in documents:
#         for chunk in document["chunks"]:
#             chunks.append(
#                 {
#                     "document_id": document["document_id"],
#                     "chunk_id": chunk["chunk_id"],
#                     "text": chunk["text"],
#                 }
#             )

#     return chunks


# def main() -> None:
#     parser = argparse.ArgumentParser()
#     parser.add_argument("command", choices=["extract"])
#     parser.add_argument("--profile", required=True)
#     parser.add_argument("--input", required=True)
#     parser.add_argument("--model", default=None)
#     parser.add_argument("--output-dir", default="runs")
#     args = parser.parse_args()

#     profile = load_profile(args.profile)
#     chunks = load_documents(args.input)

#     output_dir = Path(args.output_dir)
#     output_dir.mkdir(parents=True, exist_ok=True)

#     for chunk in chunks:
#         print(f"Extracting {chunk['chunk_id']}...")

#         extraction = extract_from_chunk(
#             profile=profile,
#             chunk=chunk,
#             model_tag=args.model,
#         )

#         validation = validate_extraction(
#             extraction=extraction,
#             source_text=chunk["text"],
#             expected_chunk_id=chunk["chunk_id"],
#         )

#         record = {
#             **extraction,
#             "validation": validation,
#             "created_at": datetime.now(timezone.utc).isoformat(),
#         }

#         output_path = output_dir / f"{chunk['chunk_id'].replace(':', '__')}.json"

#         with open(output_path, "w", encoding="utf-8") as file:
#             json.dump(record, file, indent=2, ensure_ascii=False)

#         status = "PASS" if validation["all_quotes_verified"] else "FAIL"
#         print(f"{status}: {output_path}")

#         if not validation["all_quotes_verified"]:
#             print(json.dumps(validation["failures"], indent=2))


# if __name__ == "__main__":
#     main()