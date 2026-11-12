
import { API_BASE_URL, getAuthHeaders } from "../api";

// Get all internship batches
export async function getInternshipBatches() {
    const response = await fetch(`${API_BASE_URL}/internship-batches/`, {
        method: "GET",
        headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Create an internship batch
export async function createInternshipBatch(batchData) {
    const response = await fetch(`${API_BASE_URL}/internship-batches/`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(batchData),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Update an internship batch
export async function updateInternshipBatch(batchId, batchData) {
    const response = await fetch(
        `${API_BASE_URL}/internship-batches/detail/${batchId}/`,
        {
            method: "PATCH",
            headers: getAuthHeaders(),
            body: JSON.stringify(batchData),
        }
    );

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Delete an internship batch
export async function deleteInternshipBatch(batchId) {
    const response = await fetch(
        `${API_BASE_URL}/internship-batches/detail/${batchId}/`,
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
