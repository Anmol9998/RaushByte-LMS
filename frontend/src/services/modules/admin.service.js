
import { API_BASE_URL, getAuthHeaders } from "../api";

// Admin dashboard summary
export async function getDashboardSummary() {
    const response = await fetch(`${API_BASE_URL}/admin/dashboard/`, {
        method: "GET",
        headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Get all users
export async function getUsers() {
    const response = await fetch(`${API_BASE_URL}/admin/users/`, {
        method: "GET",
        headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Create a user
export async function createUser(userData) {
    const response = await fetch(`${API_BASE_URL}/admin/users/`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(userData),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Update user
export async function updateUser(userId, userData) {
    const response = await fetch(
        `${API_BASE_URL}/admin/users/${userId}/`,
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

// Delete user
export async function deleteUser(userId) {
    const response = await fetch(
        `${API_BASE_URL}/admin/users/${userId}/`,
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
