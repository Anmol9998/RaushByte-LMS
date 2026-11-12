
import { API_BASE_URL } from "./api";

// Register a new user
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

// Login user
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
