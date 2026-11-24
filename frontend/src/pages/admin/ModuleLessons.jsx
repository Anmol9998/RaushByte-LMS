
import { useEffect, useRef, useState } from "react";
import "./ModuleLessons.css";

import {
    ArrowLeft,
    Plus,
    BookOpen,
    X,
    FileVideo,
    FileText,
} from "lucide-react";

import {
    getLessons,
    getModules,
    createLesson,
    updateLesson,
    deleteLesson,
    uploadLessonFile,
} from "../../services/modules/courses.service";

function ModuleLessons({ moduleId, onBack }) {
    const [module, setModule] = useState(null);
    const [lessons, setLessons] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [showLessonForm, setShowLessonForm] = useState(false);
    const [savingLesson, setSavingLesson] = useState(false);
    const [editingLesson, setEditingLesson] = useState(null);

    const [lessonForm, setLessonForm] = useState({
        title: "",
        description: "",
        content_type: "video",
        text_content: "",
        external_link: "",
    });

    const [selectedVideo, setSelectedVideo] = useState(null);
    const [videoPreview, setVideoPreview] = useState("");
    const [selectedDocument, setSelectedDocument] = useState(null);

    const videoInputRef = useRef(null);
    const documentInputRef = useRef(null);

    // Load module and its lessons
    async function loadModuleLessons() {
        try {
            setLoading(true);
            setError("");

            const [moduleData, lessonData] = await Promise.all([
                getModules(),
                getLessons(),
            ]);

            const allModules = Array.isArray(moduleData)
                ? moduleData
                : moduleData.results || [];

            const selectedModule = allModules.find(
                (item) => String(item.id) === String(moduleId)
            );

            if (!selectedModule) {
                throw new Error("Module not found.");
            }

            setModule(selectedModule);

            const allLessons = Array.isArray(lessonData)
                ? lessonData
                : lessonData.results || [];

            const moduleLessons = allLessons.filter(
                (lesson) =>
                    String(lesson.module?.id || lesson.module) ===
                    String(moduleId)
            );

            setLessons(moduleLessons);
        } catch (err) {
            console.error("Lesson loading error:", err);
            setError("Unable to load module lessons.");
        } finally {
            setLoading(false);
        }
    }

    // Clear selected files
    function clearSelectedFiles() {
        if (videoPreview) {
            URL.revokeObjectURL(videoPreview);
        }

        setSelectedVideo(null);
        setVideoPreview("");
        setSelectedDocument(null);

        if (videoInputRef.current) {
            videoInputRef.current.value = "";
        }

        if (documentInputRef.current) {
            documentInputRef.current.value = "";
        }
    }

    // Reset lesson form
    function resetLessonForm() {
        clearSelectedFiles();

        setLessonForm({
            title: "",
            description: "",
            content_type: "video",
            text_content: "",
            external_link: "",
        });

        setEditingLesson(null);
        setShowLessonForm(false);
    }

    // Handle content type change
    function handleContentTypeChange(value) {
        clearSelectedFiles();

        setLessonForm((previous) => ({
            ...previous,
            content_type: value,
        }));
    }

    // Handle lesson submission


    async function handleLessonSubmit(event) {
        event.preventDefault();

        // Validate required file selection
        if (
            lessonForm.content_type === "video" &&
            !editingLesson &&
            !selectedVideo
        ) {
            alert("Please select a video for this lesson.");
            return;
        }

        if (
            ["pdf", "ppt"].includes(lessonForm.content_type) &&
            !editingLesson &&
            !selectedDocument
        ) {
            alert(`Please select a ${lessonForm.content_type.toUpperCase()} file.`);
            return;
        }

        try {
            setSavingLesson(true);

            const lessonData = {
                module: moduleId,
                title: lessonForm.title.trim(),
                description: lessonForm.description.trim(),
                content_type: lessonForm.content_type,
                text_content: lessonForm.text_content,
                external_link: lessonForm.external_link,
                order: editingLesson
                    ? editingLesson.order
                    : lessons.length > 0
                        ? Math.max(...lessons.map(lesson => lesson.order || 0)) + 1
                        : 1,
                is_active: true,
            };

            let savedLesson;

            // Create or update lesson
            if (editingLesson) {
                savedLesson = await updateLesson(
                    editingLesson.id,
                    lessonData
                );
            } else {
                savedLesson = await createLesson(lessonData);
            }

            // Upload video, PDF or PPT to Cloudflare R2
            const fileToUpload =
                lessonForm.content_type === "video"
                    ? selectedVideo
                    : ["pdf", "ppt"].includes(lessonForm.content_type)
                        ? selectedDocument
                        : null;

            if (fileToUpload) {
                savedLesson = await uploadLessonFile(
                    savedLesson.id,
                    fileToUpload
                );
            }

            // Update lesson list
            if (editingLesson) {
                setLessons(previous =>
                    previous.map(lesson =>
                        String(lesson.id) === String(editingLesson.id)
                            ? savedLesson
                            : lesson
                    )
                );
            } else {
                setLessons(previous => [...previous, savedLesson]);
            }

            resetLessonForm();
            alert("Lesson saved successfully!");

        } catch (err) {
            console.error("Lesson save/upload error:", err);
            alert("Unable to save the lesson or upload its file. Please check the console.");
        } finally {
            setSavingLesson(false);
        }
    }



    // Edit lesson
    function handleEditLesson(lesson) {
        clearSelectedFiles();

        setEditingLesson(lesson);

        setLessonForm({
            title: lesson.title || "",
            description: lesson.description || "",
            content_type: lesson.content_type || "video",
            text_content: lesson.text_content || "",
            external_link: lesson.external_link || "",
        });

        setShowLessonForm(true);
    }

    // Delete lesson
    async function handleDeleteLesson(lesson) {
        const confirmed = window.confirm(
            `Are you sure you want to delete "${lesson.title}"?`
        );

        if (!confirmed) return;

        try {
            await deleteLesson(lesson.id);

            setLessons((previous) =>
                previous.filter((item) => item.id !== lesson.id)
            );
        } catch (err) {
            console.error("Lesson deletion error:", err);
            alert("Unable to delete lesson. Please try again.");
        }
    }

    // Handle video selection
    function handleVideoChange(event) {
        const file = event.target.files[0];

        if (!file) return;

        if (!file.type.startsWith("video/")) {
            alert("Please select a valid video file.");
            event.target.value = "";
            return;
        }

        const maxSize = 500 * 1024 * 1024; // 500 MB

        if (file.size > maxSize) {
            alert("Video size should not exceed 500 MB.");
            event.target.value = "";
            return;
        }

        if (videoPreview) {
            URL.revokeObjectURL(videoPreview);
        }

        setSelectedVideo(file);
        setVideoPreview(URL.createObjectURL(file));
    }

    // Remove selected video
    function removeVideo() {
        if (videoPreview) {
            URL.revokeObjectURL(videoPreview);
        }

        setSelectedVideo(null);
        setVideoPreview("");

        if (videoInputRef.current) {
            videoInputRef.current.value = "";
        }
    }

    // Handle PDF/PPT selection
    function handleDocumentChange(event) {
        const file = event.target.files[0];

        if (!file) return;

        const maxSize = 50 * 1024 * 1024; // 50 MB

        const isValid =
            lessonForm.content_type === "pdf"
                ? file.type === "application/pdf" ||
                file.name.toLowerCase().endsWith(".pdf")
                : /\.(ppt|pptx)$/i.test(file.name);

        if (!isValid) {
            alert(
                lessonForm.content_type === "pdf"
                    ? "Please select a valid PDF file."
                    : "Please select a valid PPT or PPTX file."
            );

            event.target.value = "";
            return;
        }

        if (file.size > maxSize) {
            alert("File size should not exceed 50 MB.");
            event.target.value = "";
            return;
        }

        setSelectedDocument(file);
    }

    // Remove selected document
    function removeDocument() {
        setSelectedDocument(null);

        if (documentInputRef.current) {
            documentInputRef.current.value = "";
        }
    }

    useEffect(() => {
        loadModuleLessons();
    }, [moduleId]);

    return (
        <div className="module-lessons">
            <button type="button" onClick={onBack}>
                <ArrowLeft size={17} />
                Back to Modules
            </button>

            <div className="module-lessons-heading">
                <div>
                    <p>MODULE CONTENT</p>

                    <h1>{module?.title || "Module Lessons"}</h1>

                    <span>
                        {module?.description ||
                            "Manage lessons in this module."}
                    </span>
                </div>

                <button
                    type="button"
                    onClick={() => {
                        resetLessonForm();
                        setShowLessonForm(true);
                    }}
                >
                    <Plus size={17} />
                    Add Lesson
                </button>
            </div>

            {/* Add / Edit Lesson Form */}
            {showLessonForm && (
                <div className="lesson-form">
                    <h2>
                        {editingLesson ? "Edit Lesson" : "Add New Lesson"}
                    </h2>

                    <form onSubmit={handleLessonSubmit}>
                        {/* Lesson Title */}
                        <label>
                            Lesson Title

                            <input
                                type="text"
                                value={lessonForm.title}
                                onChange={(event) =>
                                    setLessonForm((previous) => ({
                                        ...previous,
                                        title: event.target.value,
                                    }))
                                }
                                placeholder="e.g. Introduction to HTML"
                                required
                            />
                        </label>

                        {/* Description */}
                        <label>
                            Description

                            <textarea
                                value={lessonForm.description}
                                onChange={(event) =>
                                    setLessonForm((previous) => ({
                                        ...previous,
                                        description: event.target.value,
                                    }))
                                }
                                placeholder="Describe what this lesson covers..."
                            />
                        </label>

                        {/* Content Type */}
                        <label>
                            Content Type

                            <select
                                value={lessonForm.content_type}
                                onChange={(event) =>
                                    handleContentTypeChange(
                                        event.target.value
                                    )
                                }
                            >
                                <option value="video">Video</option>
                                <option value="pdf">PDF</option>
                                <option value="ppt">PPT</option>
                                <option value="text">Text</option>
                                <option value="link">Link</option>
                                <option value="quiz">Quiz</option>
                                <option value="assignment">Assignment</option>
                            </select>
                        </label>

                        {/* Video Upload */}
                        {lessonForm.content_type === "video" && (
                            <div className="lesson-upload-section">
                                <label htmlFor="lesson-video">
                                    Upload Lesson Video
                                </label>

                                <input
                                    ref={videoInputRef}
                                    id="lesson-video"
                                    type="file"
                                    accept="video/*"
                                    onChange={handleVideoChange}
                                />

                                {selectedVideo && (
                                    <div className="selected-video">
                                        <FileVideo size={20} />

                                        <span>{selectedVideo.name}</span>

                                        <button
                                            type="button"
                                            onClick={removeVideo}
                                            title="Remove video"
                                        >
                                            <X size={16} />
                                        </button>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Video Preview */}
                        {selectedVideo && videoPreview && (
                            <div className="video-preview">
                                <video
                                    src={videoPreview}
                                    controls
                                    width="100%"
                                />
                            </div>
                        )}

                        {/* PDF / PPT Upload */}
                        {(lessonForm.content_type === "pdf" ||
                            lessonForm.content_type === "ppt") && (
                                <div className="lesson-upload-section">
                                    <label htmlFor="lesson-document">
                                        Upload{" "}
                                        {lessonForm.content_type.toUpperCase()} File
                                    </label>

                                    <input
                                        ref={documentInputRef}
                                        id="lesson-document"
                                        type="file"
                                        accept={
                                            lessonForm.content_type === "pdf"
                                                ? ".pdf,application/pdf"
                                                : ".ppt,.pptx,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                        }
                                        onChange={handleDocumentChange}
                                    />

                                    {selectedDocument && (
                                        <div className="selected-video">
                                            <FileText size={20} />

                                            <span>{selectedDocument.name}</span>

                                            <button
                                                type="button"
                                                onClick={removeDocument}
                                                title="Remove document"
                                            >
                                                <X size={16} />
                                            </button>
                                        </div>
                                    )}
                                </div>
                            )}

                        {/* Text Content */}
                        {lessonForm.content_type === "text" && (
                            <label className="lesson-text-section">
                                Lesson Content

                                <textarea
                                    value={lessonForm.text_content}
                                    onChange={(event) =>
                                        setLessonForm((previous) => ({
                                            ...previous,
                                            text_content: event.target.value,
                                        }))
                                    }
                                    placeholder="Write your lesson content here..."
                                    rows={8}
                                    required
                                />
                            </label>
                        )}


                        {/* Save Button */}
                        <button type="submit" disabled={savingLesson}>
                            {savingLesson
                                ? "Saving..."
                                : editingLesson
                                    ? "Update Lesson"
                                    : "Save Lesson"}
                        </button>

                        {/* Cancel Button */}
                        <button
                            type="button"
                            onClick={resetLessonForm}
                            disabled={savingLesson}
                        >
                            Cancel
                        </button>
                    </form>
                </div>
            )}

            {/* Lesson List */}
            <div className="lesson-list">
                {loading ? (
                    <p>Loading lessons...</p>
                ) : error ? (
                    <p>{error}</p>
                ) : lessons.length === 0 ? (
                    <div>
                        <BookOpen size={36} />
                        <h2>No lessons added yet</h2>
                        <p>
                            Start building this module by adding your first
                            lesson.
                        </p>
                    </div>
                ) : (
                    lessons.map((lesson) => (
                        <div className="lesson-card" key={lesson.id}>
                            <div>
                                <span>Lesson {lesson.order}</span>
                                <h3>{lesson.title}</h3>
                                <p>{lesson.description}</p>
                            </div>

                            <span className="lesson-content-type">
                                {lesson.content_type}
                            </span>

                            <button
                                type="button"
                                className="lesson-edit-button"
                                onClick={() => handleEditLesson(lesson)}
                            >
                                Edit
                            </button>

                            <button
                                type="button"
                                className="lesson-delete-button"
                                onClick={() => handleDeleteLesson(lesson)}
                                title="Delete lesson"
                            >
                                Delete
                            </button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default ModuleLessons;
