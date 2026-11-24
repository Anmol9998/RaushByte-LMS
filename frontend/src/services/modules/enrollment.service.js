
import { API_BASE_URL, getAuthHeaders } from "../api";

export async function enrollInCourse(courseId) {
    const response = await fetch(
        `${API_BASE_URL}/students/enrollments/`,
        {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify({
                course: courseId,
            }),
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw data;
    }

    return data;
}

export async function getMyEnrollments() {
    const response = await fetch(
        `${API_BASE_URL}/students/enrollments/`,
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
