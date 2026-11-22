import { useAuth } from "../auth";

export default function Home() {
  const { user, logout } = useAuth();
  return (
    <div style={{ padding: 32 }}>
      <h1>NarrativeVoice</h1>
      <p>Welcome, {user}.</p>
      <button onClick={logout}>Log out</button>
    </div>
  );
}