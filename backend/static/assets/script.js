// backend/static/assets/script.js
const API_BASE = window.location.origin + "/api";

async function register({ fname, lname, email, mobile, password, confirmPassword }) {
  try {
    const res = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fname, lname, email, mobile, password, confirmPassword })
    });
    return await res.json();
  } catch (err) {
    console.error(err);
    return { message: "Network error" };
  }
}

async function login({ email, password }) {
  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (data.token) localStorage.setItem("token", data.token);
    return data;
  } catch (err) {
    console.error(err);
    return { message: "Network error" };
  }
}

async function me() {
  const token = localStorage.getItem("token");
  if (!token) return { message: "No token" };
  try {
    const res = await fetch(`${API_BASE}/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return await res.json();
  } catch (err) {
    console.error(err);
    return { message: "Network error" };
  }
}

// Expose for console/testing
window.register = register;
window.login = login;
window.me = me;
