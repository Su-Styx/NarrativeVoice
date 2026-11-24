import json
import re
from pathlib import Path
from natsort import natsorted
import pandas as pd

from .private_directories import chunk_directory


# def _natural_key(path: Path):
#     return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", path.stem)]


def load_chunk_dataframe(directory=chunk_directory) -> pd.DataFrame:
    rows = []
    for file_path in natsorted(Path(directory).glob("*.json")):
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data.get("validation", {}).get("accepted", []):
            rows.append(
                {
                    "chunk_id": str(item.get("source_chunk_id", file_path.stem)),
                    "field": item["field"],
                    "statement": str(item["statement"]).strip(),
                }
            )

    df = pd.DataFrame(rows, columns=["chunk_id", "field", "statement"])
    df = df.replace(r'^\d+:(?=chunk_)', '', regex=True)
    # regex to match until the 'chunk',

    # df = df[df["field"].str.strip() != 'stated_links']



    return df.drop_duplicates(subset=["chunk_id", "field", "statement"]).reset_index(drop=True)


if __name__ == "__main__":
    df = load_chunk_dataframe()
  
    # print(f"{len(df)} rows from {df['chunk_id'].nunique()} chunks")
    # print(df.head())