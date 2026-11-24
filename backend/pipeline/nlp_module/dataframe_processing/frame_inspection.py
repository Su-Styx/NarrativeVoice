import pandas as pd



def compute_metrics(df):
    df = df.copy()

    # rows per field
    rows_per_field = df.groupby("field").size()

    # items per chunk and field
    parts = df["chunk_id"].str.partition(":")
    df["chunk"] = parts[2].where(parts[1] != "", df["chunk_id"])
    items_per_chunk = pd.crosstab(df["chunk"], df["field"])

    # 10 most common topics, experiences, challenges, themes
    # stated_links are not quantified, they are for qualitative analysis and relationships
    top_statements = {}
    for field in ["topics", "experiences", "challenges", "themes"]:
        counts = df[df["field"] == field]["statement"].str.lower().str.strip().value_counts()
        top_statements[field] = counts.head(10).to_dict()

    return {
        "rows_per_field": rows_per_field.to_dict(),
        "items_per_chunk": items_per_chunk.to_dict(orient="index"),
        "top_statements": top_statements,
    }