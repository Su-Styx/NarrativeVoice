# bridge contact from celery wrorker/ app backend
# sensitive url routes stored in above file reference but follow this shape:
import json
import subprocess
import sys
from pathlib import Path


from .dataframe_processing.chunk_parse import load_chunk_dataframe
from .dataframe_processing.nodes import build_nodes
from .dataframe_processing.edges import build_edges, to_graph
from .dataframe_processing.frame_inspection import compute_metrics

# PIPELINE_DIR = Path(__file__).resolve().parent

PIPELINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PIPELINE_DIR / "dataframe_processing"))

def resolve(path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else (PIPELINE_DIR / p).resolve()

# temp_values={
#     'pdf':'qwen-student-experience.pdf',
#     'chunk_out':'qwen-student-experience.txt',
#     'doc-id':'[pick a number]',
#     'title':'student-experience',
#     'pages':'[enter range '0-inf']',
#     # below are parameters for extr_command
#     'profile':'per-chunk-profile.YAML',
#     'input': 'qwen-student-experience.txt',
#     'output': 'data_repo/'
# }



def run_step(name: str, command: list):
    print(f"{name} running")
    result = subprocess.run(command, capture_output=True, text=True, cwd=PIPELINE_DIR)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"{name} failed (exit code {result.returncode}):\n{result.stderr[-2000:]}")


def run_pipeline(v: dict) -> dict:
    pdf = Path(v["pdf"]).resolve()
    chunk_out = Path(v["chunk_out"]).resolve()
    extr_in = Path(v["input"]).resolve()
    extr_out = Path(v["output"]).resolve()

    run_step("chunking", [
        sys.executable, "chunking.py",
        "--pdf", str(pdf),
        "--output", str(chunk_out),
        "--document-id", v["doc-id"],
        "--title", v["title"],
        "--pages", v["pages"],
    ])
    run_step("extraction", [
        sys.executable, "engine.py", "extract",
        "--profile", v["profile"],
        "--input", str(extr_in),
        "--output-dir", str(extr_out),
    ])

    df = load_chunk_dataframe(extr_out)
    nodes = build_nodes(df)
    edges = build_edges(nodes)
    return build_result(df, nodes, edges)



def build_result(df, nodes, edges) -> dict:
    G = to_graph(nodes, edges)
    return {
        "metrics": compute_metrics(df),
        "graph": {
            "nodes": [
                {"id": n, "type": d["type"], "n_chunks": d["n_chunks"], "degree": G.degree(n)}
                for n, d in G.nodes(data=True)
            ],
            "edges": edges.to_dict(orient="records"),
        },
        "statements": df.to_dict(orient="records"),
    }

if __name__ == "__main__":
    from .api_endpoint_temp_vals import temp_values 
    # again, temp_values are imported from external secret file
    result = run_pipeline(temp_values)

    out_file = resolve(temp_values["output"]) / "result.json"
    out_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"{len(result['statements'])} rows, "
          f"{len(result['graph']['nodes'])} nodes, {len(result['graph']['edges'])} edges")
    print(f"Wrote {out_file}")