// function getCookie(name) {
//   return document.cookie
//     .split("; ")
//     .find((row) => row.startsWith(name + "="))
//     ?.split("=")[1];
// }

async function request(path, options = {}) {
  const res = await fetch(`/api${path}`, options);
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, data };
}

export function get(path) {
  return request(path);
}

export function post(path, body = {}) {
  return request(path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken") || "",
    },
    body: JSON.stringify(body),
  });
}

function authHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Token ${token}` } : {};
}

// export async function api(path, options = {}) {
//   const res = await fetch("/api" + path, {
//     ...options,
//     headers: { "Content-Type": "application/json", ...authHeaders(), ...options.headers },
//   });
//   if (!res.ok) throw new Error(`Request failed (${res.status})`);
//   return res.json();
// }

function getCookie(name) {
  const match = document.cookie.split("; ").find((c) => c.startsWith(name + "="));
  return match ? decodeURIComponent(match.split("=")[1]) : "";
}

export async function api(path, options = {}) {
  const method = (options.method || "GET").toUpperCase();
  const headers = { ...options.headers };
  if (!(options.body instanceof FormData)) headers["Content-Type"] = "application/json";
  if (method !== "GET") headers["X-CSRFToken"] = getCookie("csrftoken");

  const res = await fetch("/api" + path, { ...options, headers, credentials: "same-origin" });
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.json();
}