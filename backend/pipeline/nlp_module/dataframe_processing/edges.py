import re

import networkx as nx
import pandas as pd




def mentions(experience: str, topic: str) -> bool:
    """True if the topic appears as whole words inside the experience text."""
    return re.search(rf"\b{re.escape(topic.lower())}\b", experience.lower()) is not None


def build_edges(nodes: dict) -> pd.DataFrame:
    experiences = {label: n for label, n in nodes.items() if n["type"] == "experiences"}
    topics = {label: n for label, n in nodes.items() if n["type"] == "topics"}

    rows = []
    for e_label, e in experiences.items():
        for t_label, t in topics.items():
            shared = sorted(set(e["chunks"]) & set(t["chunks"]))
            if mentions(e_label, t_label):
                kind = "mentions"
            elif shared:
                kind = "same_chunk"
            else:
                continue
            rows.append(
                {
                    "experience": e_label,
                    "topic": t_label,
                    "kind": kind,
                    "n_shared_chunks": len(shared),
                    "shared_chunks": ",".join(shared),
                }
            )

    edges = pd.DataFrame(
        rows, columns=["experience", "topic", "kind", "n_shared_chunks", "shared_chunks"]
    )
    # 'mentions' sorts before 'same_chunk' alphabetically
    return edges.sort_values(["kind", "n_shared_chunks"], ascending=[True, False]).reset_index(drop=True)


def to_graph(nodes: dict, edges: pd.DataFrame) -> nx.Graph:
    G = nx.Graph()
    for label, n in nodes.items():
        G.add_node(label, type=n["type"], n_chunks=len(n["chunks"]))
    for r in edges.itertuples():
        G.add_edge(r.experience, r.topic, kind=r.kind, n_shared_chunks=r.n_shared_chunks)
    return G


def save(nodes: dict, edges: pd.DataFrame) -> nx.Graph:
    G = to_graph(nodes, edges)
    if out_dir is not None:
        edges.to_csv(Path(out_dir) / "edges.csv", index=False)
    # plt.show()
    # nx.draw(G, with_labels=True, node_color="lightblue", edge_color="gray")
    # plt.savefig("graph.png", dpi=300, bbox_inches="tight")  


    # nx.write_graphml(G, "graph.graphml")
    # nx.draw(G)
    # plt.show()

    print(f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(edges["kind"].value_counts().to_string())
    top = sorted(G.degree, key=lambda x: x[1], reverse=True)[:10]
    print("\nMost connected nodes:")
    for label, degree in top:
        print(f"  {degree:3d}  {label}")
    return G