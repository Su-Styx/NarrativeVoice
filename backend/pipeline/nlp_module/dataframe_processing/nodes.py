# building a relationship-graph of the identified topics and 

# build list of nodes with attributes:

import pandas as pd

from .chunk_parse import load_chunk_dataframe

NODE_TYPES = ["topics", "experiences"]


def build_nodes(df: pd.DataFrame) -> dict:
    nodes = {}
    for row in df[df["field"].isin(NODE_TYPES)].itertuples(index=False):
        node = nodes.setdefault(row.statement, {"type": row.field, "chunks": []})
        if row.chunk_id not in node["chunks"]:
            node["chunks"].append(row.chunk_id)
    return nodes


if __name__ == "__main__":
    from edges import build_edges, save

    nodes = build_nodes(load_chunk_dataframe())
    save(nodes, build_edges(nodes))