import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import LoginPage, { Username, Password, Submit, Title, Reset, Input } from "@react-login-page/page1";
import { post } from "../api";

export default function Signup() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const handleSubmit = async () => {
    setErrors({});
    const { ok, data } = await post("/register/", form);
    if (!ok) {
      setErrors(data.errors || { form: "Something went wrong." });
      return;
    }
    navigate("/login");
  };

  const messages = Object.values(errors);

  return (
    <div style={{ height: "100%" }}>
      <LoginPage style={{ height: "100%" }}>
        <Title>Create account</Title>
        <Username name="username" index={2} value={form.username} onChange={set("username")} />
        <Input name="email" type="email" index={1} placeholder="Email" value={form.email} onChange={set("email")} />
        <Password name="password" index={3} value={form.password} onChange={set("password")} />
        <Submit onClick={handleSubmit}>Sign up</Submit>
        <Reset visible={false} />
      </LoginPage>
      <div style={{ position: "fixed", bottom: 16, width: "100%", textAlign: "center" }}>
        {messages.map((m, i) => (
          <p key={i} style={{ color: "#ff7b7b", margin: "0 0 4px" }}>{m}</p>
        ))}
        <p style={{ margin: "8px 0 0" }}>
          Already registered? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  );
}