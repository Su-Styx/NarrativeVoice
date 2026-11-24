import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";

export default function DocumentView() {
  const { id } = useParams();
  const [doc, setDoc] = useState(null);

  useEffect(() => {
    api(`/documents/${id}/`).then(setDoc);
  }, [id]);

  if (!doc) return <p style={{ padding: 32 }}>Loading...</p>;

  return (
    <div style={{ padding: 32 }}>
      <Link to="/">Back</Link>
      <h2>{doc.title}</h2>
      <p>Status: {doc.status}</p>
      <pre style={{ whiteSpace: "pre-wrap" }}>{doc.text}</pre>
    </div>
  );
}