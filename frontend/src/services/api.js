const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

export async function registerUser(formData) {
  const response = await fetch(`${API_BASE_URL}/auth/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw data;
  }

  return data;
}

export async function loginUser(formData) {
  const response = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw data;
  }

  return data;
}
function getAuthHeaders() {
  const token = localStorage.getItem("access");

  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}
export async function getDashboardSummary() {
  const response = await fetch(
    `${API_BASE_URL}/auth/admin/dashboard/`,
    {
      method: "GET",
      headers: getAuthHeaders(),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw data;
  }

  return data;
}