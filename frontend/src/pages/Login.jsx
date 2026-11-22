import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import LoginPage, { Username, Password, Submit, Title, Reset } from "@react-login-page/page1";
import { useAuth } from "../auth";
import { post } from "../api";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async () => {
    setError("");
    const { ok, data } = await post("/login/", { username, password });
    if (!ok) {
      setError(data.errors?.form || "Something went wrong.");
      return;
    }
    login(data.username); // stub until tokens/sessions
    navigate("/");
  };

  return (
    <div style={{ height: "100%" }}>
      <LoginPage style={{ height: "100%" }}>
        <Title>NarrativeVoice</Title>
        <Username name="username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <Password name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <Submit onClick={handleSubmit}>Log in</Submit>
        <Reset visible={false} />
      </LoginPage>
      <div style={{ position: "fixed", bottom: 16, width: "100%", textAlign: "center" }}>
        {error && <p style={{ color: "#ff7b7b", margin: "0 0 8px" }}>{error}</p>}
        <p style={{ margin: 0 }}>
          No account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}