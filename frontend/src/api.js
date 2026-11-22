function getCookie(name) {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="))
    ?.split("=")[1];
}

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