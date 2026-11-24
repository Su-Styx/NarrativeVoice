import pandas as pd

from chunk_parse import load_chunk_dataframe


df = load_chunk_dataframe()

print("Rows per field")
print(df.groupby("field").size())


print("Items per chunk and field")
parts = df["chunk_id"].str.partition(":")
df["chunk"] = parts[2].where(parts[1] != "", df["chunk_id"])
print(pd.crosstab(df["chunk"], df["field"]))



# displays 10 most common topics, experiences, challenges,themes



for field in ["topics", "experiences", "challenges", "themes"]:
    print(f"\nTop 10 {field}")
    # an attempt at normalising statements 
    counts = df[df["field"] == field]["statement"].str.lower().str.strip().value_counts()
    print(counts.head(10))

    # note that stated_links are not quantified as it is only useful as qualitative analysis and analysing relationships 
    