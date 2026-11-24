import { useEffect, useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../auth";
import { api } from "../api";

export default function Home() {
  const { user, logout } = useAuth();
  const [docs, setDocs] = useState([]);
  const [file, setFile] = useState(null);
  const [inputKey, setInputKey] = useState(0);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const load = () =>
    api("/documents/").then(setDocs).catch((e) => setError(e.message));

  useEffect(() => {
    if (!user) return;
    load();
    const timer = setInterval(load, 5000);
    return () => clearInterval(timer);
  }, [user]);

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const body = new FormData();
      body.append("pdf", file);
      await api("/documents/", { method: "POST", body });
      setFile(null);
      setInputKey((k) => k + 1);
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  if (!user) return <Navigate to="/login" replace />;

  return (
    <div style={{ padding: 32 }}>
      <h1>NarrativeVoice</h1>
      <p>Welcome, {user}.</p>
      <button onClick={logout}>Log out</button>
      {error && <p>{error}</p>}

      <div style={{ display: "flex", gap: 32, marginTop: 24 }}>
        <div style={{ flex: 1, border: "1px solid #ccc", padding: 16 }}>
          <h2>Your documents</h2>
          {docs.length === 0 && <p>No documents yet.</p>}
          <ul>
            {docs.map((d) => (
              <li key={d.id}>
                <Link to={`/documents/${d.id}`}>{d.title}</Link> ({d.status})
              </li>
            ))}
          </ul>
        </div>

        <form onSubmit={submit} style={{ flex: 1, border: "1px solid #ccc", padding: 16 }}>
          <h2>Upload a PDF</h2>
          <input
            key={inputKey}
            type="file"
            accept=".pdf,application/pdf"
            onChange={(e) => setFile(e.target.files[0] || null)}
          />
          <br />
          <button type="submit" disabled={busy || !file}>
            Upload
          </button>
        </form>
      </div>
    </div>
  );
}