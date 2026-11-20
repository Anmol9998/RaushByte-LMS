
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


// Get a single course by ID
export async function getCourseById(courseId) {
    const response = await fetch(
        `${API_BASE_URL}/courses/detail/${courseId}/`,
        {
            method: "GET",
            headers: getAuthHeaders(),
        }
    );

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


// Get all modules
export async function getModules() {
    const response = await fetch(`${API_BASE_URL}/courses/modules/`, {
        method: "GET",
        headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Create a module
export async function createModule(moduleData) {
    const response = await fetch(`${API_BASE_URL}/courses/modules/`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(moduleData),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Delete a module
export async function deleteModule(moduleId) {
    const response = await fetch(
        `${API_BASE_URL}/courses/modules/${moduleId}/`,
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

// Update a module
export async function updateModule(moduleId, moduleData) {
    const response = await fetch(
        `${API_BASE_URL}/courses/modules/${moduleId}/`,
        {
            method: "PATCH",
            headers: getAuthHeaders(),
            body: JSON.stringify(moduleData),
        }
    );

    const data = await response.json();

    if (!response.ok) throw data;

    return data;
}


// Get all lessons
export async function getLessons() {
    const response = await fetch(`${API_BASE_URL}/courses/lessons/`, {
        method: "GET",
        headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Create a lesson
export async function createLesson(lessonData) {
    const response = await fetch(`${API_BASE_URL}/courses/lessons/`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(lessonData),
    });

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Update a lesson
export async function updateLesson(lessonId, lessonData) {
    const response = await fetch(
        `${API_BASE_URL}/courses/lessons/${lessonId}/`,
        {
            method: "PATCH",
            headers: getAuthHeaders(),
            body: JSON.stringify(lessonData),
        }
    );

    const data = await response.json();
    if (!response.ok) throw data;

    return data;
}

// Delete a lesson
export async function deleteLesson(lessonId) {
    const response = await fetch(
        `${API_BASE_URL}/courses/lessons/${lessonId}/`,
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


// Upload lesson content (video, PDF, PPT)
export async function uploadLessonFile(lessonId, file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
        `${API_BASE_URL}/courses/lessons/${lessonId}/`,
        {
            method: "PATCH",
            headers: {
                ...getAuthHeaders(),
                "Content-Type": undefined,
            },
            body: formData,
        }
    );

    const data = await response.json();

    if (!response.ok) throw data;

    return data;
}
