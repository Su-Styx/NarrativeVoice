# building a relationship-graph of the identified topics and 

# build list of nodes with attributes:

import pandas as pd

INPUT_CSV = "extractions.csv"
NODE_TYPES = ["topics", "experiences"]

df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

fs_df = (
    df.loc[df["field"].isin(NODE_TYPES), ["chunk_id", "field", "statement"]]
    .reset_index(drop=True)
)

nodes = {}
for row in fs_df.itertuples(index=False):
    if row.statement not in nodes:
        nodes[row.statement] = {"type": row.field, "chunks": []}
    if row.chunk_id not in nodes[row.statement]["chunks"]:
        nodes[row.statement]["chunks"].append(row.chunk_id)

# print(len(nodes))
# print(nodes)


from edges import build_edges, save

edges = build_edges(nodes)
G = save(nodes, edges)