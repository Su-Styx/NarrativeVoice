import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";

import { useMemo } from "react";
import ForceGraph2D from "react-force-graph-2d";


function Metrics({ metrics }) {
  const label = (s) => s.replaceAll("_", " ");
  const fields = Object.keys(metrics.rows_per_field);
  const chunks = Object.entries(metrics.items_per_chunk);

  const cell = { padding: "6px 12px", textAlign: "center", borderBottom: "1px solid #eee" };

  return (
    <section>
      <h2>Metrics</h2>

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 16 }}>
        {fields.map((f) => (
          <div key={f} style={{ border: "1px solid #ddd", borderRadius: 8, padding: "8px 16px", minWidth: 110 }}>
            <div style={{ fontSize: 24, fontWeight: 600 }}>{metrics.rows_per_field[f]}</div>
            <div style={{ fontSize: 13, color: "#666" }}>{label(f)}</div>
          </div>
        ))}
      </div>

      <h3>Items per chunk</h3>
      <table style={{ borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ ...cell, textAlign: "left" }}>Chunk</th>
            {fields.map((f) => (
              <th key={f} style={cell}>{label(f)}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {chunks.map(([chunk, counts]) => (
            <tr key={chunk}>
              <td style={{ ...cell, textAlign: "left" }}>{label(chunk)}</td>
              {fields.map((f) => (
                <td key={f} style={cell}>{counts[f] ?? 0}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}


function Graph({ nodes, edges }) {
  const data = useMemo(() => {
    const gNodes = nodes.map((n) => ({
      id: n.id ?? n.label ?? n.name,
      label: n.label ?? n.name ?? String(n.id),
      type: n.type ?? n.kind ?? n.field ?? "node",
    }));

    const idByText = new Map();
    for (const n of gNodes) {
      idByText.set(n.id, n.id);
      idByText.set(n.label, n.id);
    }

    const links = edges
      .map((e) => ({
        source: idByText.get(e.experience),
        target: idByText.get(e.topic),
        weight: e.n_shared_chunks ?? 1,
        type: e.kind ?? "",
      }))
      .filter((l) => l.source !== undefined && l.target !== undefined);

    if (links.length !== edges.length) {
      console.warn(`Dropped ${edges.length - links.length} edges with no matching node`);
    }
    return { nodes: gNodes, links };
  }, [nodes, edges]);

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, width: 1500 }}>
      <ForceGraph2D
        graphData={data}
        width={1500}
        height={1200}
        nodeAutoColorBy="type"
        nodeLabel={(n) => `${n.type}: ${n.label}`}
        linkWidth={(l) => Math.min(1 + l.weight, 5)}
        linkColor={(l) => (l.type === "same_chunk" ? "#bbb" : "#555")}
        linkLabel={(l) => l.type}
        nodeCanvasObject={(node, ctx, scale) => {
          const size = 5;
          ctx.fillStyle = node.color;
          ctx.beginPath();
          ctx.arc(node.x, node.y, size, 0, 2 * Math.PI);
          ctx.fill();
          ctx.font = `${12 / scale}px sans-serif`;
          ctx.fillStyle = "#fafafa";
          ctx.textAlign = "center";
          ctx.fillText(node.label, node.x, node.y + size + 10 / scale);
        }}
      />
    </div>
  );
}

export default function DocumentView() {
  const { id } = useParams();
  const [doc, setDoc] = useState(null);

  useEffect(() => {
    let timer;
    const load = () =>
      api(`/documents/${id}/`).then((d) => {
        setDoc(d);
        if (d.status === "pending" || d.status === "running") {
          timer = setTimeout(load, 5000);
        }
      });
    load();
    return () => clearTimeout(timer);
  }, [id]);

  if (!doc) return <p style={{ padding: 32 }}>Loading...</p>;

  const result = doc.result;
  const statements = result?.statements ?? [];
  const byField = {};
  for (const s of statements) {
    (byField[s.field] ??= []).push(s);
  }
  const nodes = result?.graph?.nodes ?? [];
  const edges = result?.graph?.edges ?? [];

  return (
    <div style={{ padding: 32 }}>
      <Link to="/">Back</Link>
      <h2>{doc.title}</h2>
      <p>Status: {doc.status}</p>

      {(doc.status === "pending" || doc.status === "running") && (
        <p>Processing. This page updates automatically.</p>
      )}

      {doc.status === "failed" && (
        <pre style={{ whiteSpace: "pre-wrap", color: "crimson" }}>{doc.error}</pre>
      )}

      {doc.status === "done" && result && (
        <>
          <h3>Metrics</h3>
          {doc.result?.metrics && <Metrics metrics={doc.result.metrics} />}

          <h3>Statements</h3>
          {Object.entries(byField).map(([field, items]) => (
            <section key={field}>
              <h4>{field} ({items.length})</h4>
              <ul>
                {items.map((s, i) => (
                  <li key={i}>
                    {s.statement} <small>[{s.chunk_id}]</small>
                  </li>
                ))}
              </ul>
            </section>
          ))}

            <h3>Graph</h3>
            <p>{nodes.length} nodes, {edges.length} edges</p>
            {nodes.length > 0 && <Graph nodes={nodes} edges={edges} />}

          <details>
            <summary>Raw result</summary>
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </details>
        </>
      )}
    </div>
  );
}