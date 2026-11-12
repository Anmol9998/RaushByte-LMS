
import { useEffect, useMemo, useState } from "react";
import {
    Search,
    Plus,
    Pencil,
    Trash2,
    X,
    BookOpen,
    RefreshCw,
    CheckCircle,
    Clock,
} from "lucide-react";

import {
    getCourses,
    createCourse,
    updateCourse,
    deleteCourse,
} from "../../services/modules/courses.service";

import "./CourseManagement.css";

const emptyForm = {
    title: "",
    description: "",
    category: "",
    duration: "",
    level: "Beginner",
    is_active: true,
};

function CourseManagement() {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [search, setSearch] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");

    const [showModal, setShowModal] = useState(false);
    const [editingCourse, setEditingCourse] = useState(null);
    const [form, setForm] = useState(emptyForm);

    async function loadCourses() {
        try {
            setLoading(true);
            setError("");

            const data = await getCourses();
            setCourses(Array.isArray(data) ? data : data.results || []);
        } catch (err) {
            console.error("Courses API error:", err);
            setError(
                err.detail ||
                "Unable to load courses. Please check your connection and permissions."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadCourses();
    }, []);

    const filteredCourses = useMemo(() => {
        return courses.filter((course) => {
            const searchText = search.toLowerCase();

            const matchesSearch = [
                course.title,
                course.category,
                course.description,
                course.level,
            ].some((value) =>
                (value || "").toLowerCase().includes(searchText)
            );

            const matchesStatus =
                statusFilter === "all" ||
                (statusFilter === "active" && course.is_active) ||
                (statusFilter === "inactive" && !course.is_active);

            return matchesSearch && matchesStatus;
        });
    }, [courses, search, statusFilter]);

    function openAddModal() {
        setEditingCourse(null);
        setForm(emptyForm);
        setError("");
        setShowModal(true);
    }

    function openEditModal(course) {
        setEditingCourse(course);
        setForm({
            title: course.title || "",
            description: course.description || "",
            category: course.category || "",
            duration: course.duration || "",
            level: course.level || "Beginner",
            is_active: course.is_active ?? true,
        });
        setError("");
        setShowModal(true);
    }

    function closeModal() {
        setShowModal(false);
        setEditingCourse(null);
        setForm(emptyForm);
        setError("");
    }

    function handleChange(event) {
        const { name, value, type, checked } = event.target;

        setForm((previous) => ({
            ...previous,
            [name]: type === "checkbox" ? checked : value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            setSaving(true);
            setError("");

            const courseData = {
                title: form.title.trim(),
                description: form.description.trim(),
                category: form.category.trim(),
                duration: form.duration.trim(),
                level: form.level,
                is_active: form.is_active,
            };

            if (editingCourse) {
                await updateCourse(editingCourse.id, courseData);
            } else {
                await createCourse(courseData);
            }

            closeModal();
            await loadCourses();
        } catch (err) {
            console.error("Save course error:", err);

            const messages =
                err && typeof err === "object"
                    ? Object.entries(err)
                        .map(([field, value]) =>
                            `${field}: ${Array.isArray(value) ? value.join(", ") : value}`
                        )
                        .join("\n")
                    : "";

            setError(messages || "Unable to save course. Please try again.");
        } finally {
            setSaving(false);
        }
    }

    async function handleStatusChange(course) {
        const action = course.is_active ? "deactivate" : "activate";

        if (
            !window.confirm(
                `Are you sure you want to ${action} "${course.title}"?`
            )
        ) {
            return;
        }

        try {
            setError("");

            await updateCourse(course.id, {
                is_active: !course.is_active,
            });

            await loadCourses();
        } catch (err) {
            console.error("Course status update error:", err);
            setError("Unable to update course status.");
        }
    }

    async function handleDelete(course) {
        if (
            !window.confirm(
                `Are you sure you want to delete "${course.title}"? This action cannot be undone.`
            )
        ) {
            return;
        }

        try {
            setError("");

            await deleteCourse(course.id);
            await loadCourses();
        } catch (err) {
            console.error("Delete course error:", err);
            setError("Unable to delete this course.");
        }
    }

    const totalActive = courses.filter((course) => course.is_active).length;
    const totalInactive = courses.length - totalActive;

    return (
        <div className="course-management">
            <div className="cm-heading">
                <div>
                    <p className="admin-eyebrow">ADMINISTRATION</p>
                    <h1>Course Management</h1>
                    <p className="cm-subtitle">
                        Create, organize and manage learning courses on your platform.
                    </p>
                </div>

                <button
                    className="cm-add-button"
                    type="button"
                    onClick={openAddModal}
                >
                    <Plus size={18} />
                    Add Course
                </button>
            </div>

            <div className="cm-summary-grid">
                <article className="cm-summary-card">
                    <div className="cm-summary-icon blue">
                        <BookOpen size={21} />
                    </div>
                    <div>
                        <span>Total Courses</span>
                        <h3>{courses.length}</h3>
                    </div>
                </article>

                <article className="cm-summary-card">
                    <div className="cm-summary-icon green">
                        <CheckCircle size={21} />
                    </div>
                    <div>
                        <span>Active Courses</span>
                        <h3>{totalActive}</h3>
                    </div>
                </article>

                <article className="cm-summary-card">
                    <div className="cm-summary-icon orange">
                        <Clock size={21} />
                    </div>
                    <div>
                        <span>Inactive Courses</span>
                        <h3>{totalInactive}</h3>
                    </div>
                </article>
            </div>

            <div className="cm-table-panel">
                <div className="cm-toolbar">
                    <div>
                        <h2>All Courses</h2>
                        <p>View and manage courses available on your platform.</p>
                    </div>

                    <button
                        type="button"
                        className="cm-refresh-button"
                        onClick={loadCourses}
                        disabled={loading}
                        aria-label="Refresh courses"
                    >
                        <RefreshCw size={17} />
                    </button>
                </div>

                <div className="cm-filters">
                    <label className="cm-search">
                        <Search size={18} />
                        <input
                            type="search"
                            placeholder="Search by course title or category..."
                            value={search}
                            onChange={(event) => setSearch(event.target.value)}
                        />
                    </label>

                    <select
                        value={statusFilter}
                        onChange={(event) => setStatusFilter(event.target.value)}
                        aria-label="Filter courses by status"
                        className="cm-status-filter"
                    >
                        <option value="all">All courses</option>
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                    </select>
                </div>

                {error && !showModal && <div className="cm-error">{error}</div>}

                {loading ? (
                    <div className="cm-empty">
                        <RefreshCw size={24} className="cm-spinner" />
                        <p>Loading courses...</p>
                    </div>
                ) : filteredCourses.length === 0 ? (
                    <div className="cm-empty">
                        <BookOpen size={30} />
                        <h3>No courses found</h3>
                        <p>
                            {courses.length === 0
                                ? "Your courses will appear here once you add them."
                                : "Try changing your search or status filter."}
                        </p>
                    </div>
                ) : (
                    <div className="cm-table-wrapper">
                        <table className="cm-table">
                            <thead>
                                <tr>
                                    <th>Course</th>
                                    <th>Category</th>
                                    <th>Duration</th>
                                    <th>Level</th>
                                    <th>Mentor</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>

                            <tbody>
                                {filteredCourses.map((course) => (
                                    <tr key={course.id}>
                                        <td>
                                            <div className="cm-course-cell">
                                                <div className="cm-course-icon">
                                                    <BookOpen size={19} />
                                                </div>
                                                <div>
                                                    <strong>{course.title}</strong>
                                                    <small>{course.description}</small>
                                                </div>
                                            </div>
                                        </td>

                                        <td>{course.category}</td>
                                        <td>{course.duration}</td>
                                        <td>
                                            <span className={`cm-level ${course.level?.toLowerCase()}`}>
                                                {course.level}
                                            </span>
                                        </td>
                                        <td>{course.mentor?.name || "Not assigned"}</td>
                                        <td>
                                            <span
                                                className={`cm-status ${course.is_active ? "active" : "inactive"
                                                    }`}
                                            >
                                                {course.is_active ? "Active" : "Inactive"}
                                            </span>
                                        </td>
                                        <td>
                                            <div className="cm-actions">
                                                <button
                                                    type="button"
                                                    title="Edit course"
                                                    onClick={() => openEditModal(course)}
                                                >
                                                    <Pencil size={16} />
                                                </button>

                                                <button
                                                    type="button"
                                                    title={
                                                        course.is_active
                                                            ? "Deactivate course"
                                                            : "Activate course"
                                                    }
                                                    onClick={() => handleStatusChange(course)}
                                                >
                                                    <CheckCircle size={16} />
                                                </button>

                                                <button
                                                    type="button"
                                                    className="delete"
                                                    title="Delete course"
                                                    onClick={() => handleDelete(course)}
                                                >
                                                    <Trash2 size={16} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                <div className="cm-table-footer">
                    Showing {filteredCourses.length} of {courses.length} courses
                </div>
            </div>

            {showModal && (
                <div className="cm-modal-backdrop" onClick={closeModal}>
                    <div
                        className="cm-modal"
                        onClick={(event) => event.stopPropagation()}
                    >
                        <div className="cm-modal-heading">
                            <div>
                                <h2>{editingCourse ? "Edit Course" : "Add New Course"}</h2>
                                <p>
                                    {editingCourse
                                        ? "Update the course information."
                                        : "Add a new course to your learning platform."}
                                </p>
                            </div>

                            <button
                                type="button"
                                onClick={closeModal}
                                aria-label="Close modal"
                            >
                                <X size={20} />
                            </button>
                        </div>

                        {error && <div className="cm-error">{error}</div>}

                        <form onSubmit={handleSubmit}>
                            <div className="cm-form-grid">
                                <label className="full">
                                    Course title
                                    <input
                                        name="title"
                                        value={form.title}
                                        onChange={handleChange}
                                        required
                                        maxLength={200}
                                        placeholder="e.g. Full Stack Web Development"
                                    />
                                </label>

                                <label className="full">
                                    Description
                                    <textarea
                                        name="description"
                                        value={form.description}
                                        onChange={handleChange}
                                        required
                                        rows={4}
                                        placeholder="Describe what students will learn..."
                                    />
                                </label>

                                <label>
                                    Category
                                    <input
                                        name="category"
                                        value={form.category}
                                        onChange={handleChange}
                                        required
                                        maxLength={100}
                                        placeholder="e.g. Web Development"
                                    />
                                </label>

                                <label>
                                    Duration
                                    <input
                                        name="duration"
                                        value={form.duration}
                                        onChange={handleChange}
                                        required
                                        maxLength={100}
                                        placeholder="e.g. 12 Weeks"
                                    />
                                </label>

                                <label className="full">
                                    Course level
                                    <select
                                        name="level"
                                        value={form.level}
                                        onChange={handleChange}
                                    >
                                        <option value="Beginner">Beginner</option>
                                        <option value="Intermediate">Intermediate</option>
                                        <option value="Advanced">Advanced</option>
                                    </select>
                                </label>

                                <label className="cm-checkbox-label full">
                                    <input
                                        type="checkbox"
                                        name="is_active"
                                        checked={form.is_active}
                                        onChange={handleChange}
                                    />
                                    Make this course active
                                </label>
                            </div>

                            <div className="cm-modal-actions">
                                <button
                                    type="button"
                                    className="cm-cancel-button"
                                    onClick={closeModal}
                                    disabled={saving}
                                >
                                    Cancel
                                </button>

                                <button
                                    type="submit"
                                    className="cm-save-button"
                                    disabled={saving}
                                >
                                    {saving
                                        ? "Saving..."
                                        : editingCourse
                                            ? "Save Changes"
                                            : "Create Course"}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default CourseManagement;

