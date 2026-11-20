
import "./CourseContentManagement.css";

import { useEffect, useState } from "react";
import {
    ArrowLeft,
    ArrowRight,
    Folder,
    Plus,
    Trash2,
} from "lucide-react";
import {
    getCourseById,
    getModules,
    createModule,
    deleteModule,
    updateModule,
} from "../../services/modules/courses.service";

function CourseContentManagement({ courseId, onBack, onManageLessons }) {
    const [course, setCourse] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [modules, setModules] = useState([]);
    const [showModuleForm, setShowModuleForm] = useState(false);
    const [savingModule, setSavingModule] = useState(false);
    const [editingModule, setEditingModule] = useState(null);
    const [moduleForm, setModuleForm] = useState({
        title: "",
        description: "",
    });

    async function handleModuleSubmit(event) {
        event.preventDefault();

        try {
            setSavingModule(true);

            const moduleData = {
                course: courseId,
                title: moduleForm.title.trim(),
                description: moduleForm.description.trim(),
                order: modules.length > 0
                    ? Math.max(...modules.map((module) => module.order)) + 1
                    : 1,
                is_active: true,
            };

            if (editingModule) {
                const updatedModule = await updateModule(
                    editingModule.id,
                    {
                        title: moduleData.title,
                        description: moduleData.description,
                    }
                );

                setModules((previous) =>
                    previous.map((module) =>
                        module.id === editingModule.id
                            ? updatedModule
                            : module
                    )
                );
            } else {
                const newModule = await createModule(moduleData);
                setModules((previous) => [...previous, newModule]);
            }

            setModuleForm({
                title: "",
                description: "",
            });
            setEditingModule(null);

            setShowModuleForm(false);
        } catch (err) {
            console.error("Module creation error:", err);
            alert(
                editingModule
                    ? "Unable to update module. Please try again."
                    : "Unable to create module. Please try again."
            );
        } finally {
            setSavingModule(false);
        }
    }

    async function handleDeleteModule(module) {
        const confirmed = window.confirm(
            `Are you sure you want to delete "${module.title}"?`
        );

        if (!confirmed) return;

        try {
            await deleteModule(module.id);

            setModules((previous) =>
                previous.filter((item) => item.id !== module.id)
            );
        } catch (err) {
            console.error("Module deletion error:", err);
            alert("Unable to delete module. Please try again.");
        }
    }

    function handleEditModule(module) {
        setEditingModule(module);

        setModuleForm({
            title: module.title || "",
            description: module.description || "",
        });

        setShowModuleForm(true);
    }



    async function loadCourse() {
        try {
            setLoading(true);
            setError("");

            const data = await getCourseById(courseId);
            const courseData = Array.isArray(data) ? data[0] : data;
            setCourse(courseData);

            const moduleData = await getModules();

            const allModules = Array.isArray(moduleData)
                ? moduleData
                : moduleData.results || [];

            const courseModules = allModules.filter(
                (module) =>
                    String(module.course?.id || module.course) === String(courseId)
            );

            setModules(courseModules);

        } catch (err) {
            console.error("Course loading error:", err);
            setError("Unable to load course details.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadCourse();
    }, [courseId]);

    if (loading) {
        return <p>Loading course content...</p>;
    }

    if (error) {
        return (
            <div>
                <p>{error}</p>
                <button onClick={loadCourse}>Try Again</button>
                <button onClick={onBack}>Back to Courses</button>
            </div>
        );
    }

    if (!course) return null;

    return (
        <div className="course-content-management">
            <button type="button" onClick={onBack}>
                <ArrowLeft size={17} />
                Back to Courses
            </button>

            <div className="course-content-heading">
                <div>
                    <p>COURSE CONTENT</p>
                    <h1>{course.title}</h1>
                    <span>{course.description}</span>
                </div>

                <button
                    type="button"
                    onClick={() => setShowModuleForm(true)}
                >
                    <Plus size={17} />
                    Add Module
                </button>
            </div>

            {/* Add Module Form */}
            {showModuleForm && (
                <div className="course-module-form">
                    <h2>{editingModule ? "Edit Module" : "Add New Module"}</h2>

                    <form onSubmit={handleModuleSubmit}>
                        <label>
                            Module Title
                            <input
                                type="text"
                                value={moduleForm.title}
                                onChange={(event) =>
                                    setModuleForm({
                                        ...moduleForm,
                                        title: event.target.value,
                                    })
                                }
                                placeholder="e.g. Introduction to HTML"
                                required
                            />
                        </label>

                        <label>
                            Description
                            <textarea
                                value={moduleForm.description}
                                onChange={(event) =>
                                    setModuleForm({
                                        ...moduleForm,
                                        description: event.target.value,
                                    })
                                }
                                placeholder="Describe what this module covers..."
                            />
                        </label>

                        <button type="submit" disabled={savingModule}>
                            {savingModule
                                ? "Saving..."
                                : editingModule
                                    ? "Update Module"
                                    : "Save Module"}
                        </button>

                        <button
                            type="button"
                            onClick={() => {
                                setShowModuleForm(false);
                                setEditingModule(null);
                                setModuleForm({
                                    title: "",
                                    description: "",
                                });
                            }}
                            disabled={savingModule}
                        >
                            Cancel
                        </button>
                    </form>
                </div>
            )}

            {modules.length === 0 ? (
                <div className="course-content-empty">
                    <Folder size={36} />
                    <h2>No modules added yet</h2>
                    <p>Start organizing this course by adding your first module.</p>
                </div>
            ) : (
                <div className="course-module-list">
                    {modules.map((module) => (
                        <div className="course-module-card" key={module.id}>
                            <div>
                                <h3>{module.title}</h3>
                                <p>{module.description}</p>
                            </div>

                            <button
                                type="button"
                                className="course-module-open"
                                onClick={() => onManageLessons(module.id)}
                            >
                                Manage Lessons
                                <ArrowRight size={16} />
                            </button>

                            <button
                                type="button"
                                className="course-module-edit"
                                onClick={() => handleEditModule(module)}
                                title="Edit module"
                            >
                                Edit
                            </button>

                            <button
                                type="button"
                                className="course-module-delete"
                                onClick={() => handleDeleteModule(module)}
                                title="Delete module"
                            >
                                <Trash2 size={17} />
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default CourseContentManagement;
