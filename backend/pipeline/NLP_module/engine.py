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

import sys
from pathlib import Path

from .data_ingest import data_ingest

DEFAULT_PATH = Path(__file__).parent / "data_repo" / "Hamlet-PDF.txt"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH

    # section 0 - data ingestion
    entity = data_ingest(path)
    print(f"entity {entity.entity_id}: {len(entity.text)} chars, {len(entity.chunks)} chunks")
    for c in entity.chunks:
        print(f"  chunk {c.chunk_id} [{c.start}:{c.end}] {c.text[:60]!r}")

    print("finished executing")


if __name__ == "__main__":
    main()