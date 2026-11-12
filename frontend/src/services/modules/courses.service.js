
import { API_BASE_URL, getAuthHeaders } from "../api";

// Get all courses
export async function getCourses() {
    const response = await fetch(`${API_BASE_URL}/courses/`, {
        method: "GET",
        headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Create a course
export async function createCourse(courseData) {
    const response = await fetch(`${API_BASE_URL}/courses/`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(courseData),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Update course
export async function updateCourse(courseId, courseData) {
    const response = await fetch(
        `${API_BASE_URL}/courses/detail/${courseId}/`,
        {
            method: "PATCH",
            headers: getAuthHeaders(),
            body: JSON.stringify(courseData),
        }
    );

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Delete course
export async function deleteCourse(courseId) {
    const response = await fetch(
        `${API_BASE_URL}/courses/detail/${courseId}/`,
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
