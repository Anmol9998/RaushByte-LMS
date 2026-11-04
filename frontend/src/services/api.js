
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

// Authentication
export async function registerUser(formData) {
  const response = await fetch(`${API_BASE_URL}/auth/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  const data = await response.json();

  if (!response.ok) throw data;

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

  if (!response.ok) throw data;

  return data;
}

// Common authorization headers
function getAuthHeaders() {
  const token = localStorage.getItem("access");

  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

// Dashboard summary
export async function getDashboardSummary() {
  const response = await fetch(
    `${API_BASE_URL}/auth/admin/dashboard/`,
    {
      method: "GET",
      headers: getAuthHeaders(),
    }
  );

  const data = await response.json();

  if (!response.ok) throw data;

  return data;
}

// Get all users
export async function getUsers() {
  const response = await fetch(`${API_BASE_URL}/auth/users/`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) throw data;

  return data;
}

// Create a new user
export async function createUser(userData) {
  const response = await fetch(`${API_BASE_URL}/auth/users/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(userData),
  });

  const data = await response.json();

  if (!response.ok) throw data;

  return data;
}

// Update user details
export async function updateUser(userId, userData) {
  const response = await fetch(
    `${API_BASE_URL}/auth/users/${userId}/`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
      body: JSON.stringify(userData),
    }
  );

  const data = await response.json();

  if (!response.ok) throw data;

  return data;
}

// Delete a user
export async function deleteUser(userId) {
  const response = await fetch(
    `${API_BASE_URL}/auth/users/${userId}/`,
    {
      method: "DELETE",
      headers: getAuthHeaders(),
    }
  );

  if (!response.ok) {
    const data = await response.json();
    throw data;
  }

  return true;
}
