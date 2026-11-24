
import { useEffect, useState } from "react";
import { useNavigate, useParams, useLocation } from "react-router-dom";

import {
    enrollInCourse,
    getMyEnrollments,
} from "../../services/modules/enrollment.service";

import {
    ArrowLeft,
    BookOpen,
    Clock,
    BarChart3,
    ChevronDown,
    ChevronUp,
    PlayCircle,
    FileText,
    Presentation,
    Link as LinkIcon,
    CheckCircle,
} from "lucide-react";

import {
    getCourseById,
    getModules,
    getLessons,
} from "../../services/modules/courses.service";

import "./CourseDetails.css";

function CourseDetails() {
    const { courseId } = useParams();
    const navigate = useNavigate();
    const location = useLocation();

    const [course, setCourse] = useState(null);
    const [modules, setModules] = useState([]);
    const [lessons, setLessons] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [curriculumError, setCurriculumError] = useState("");

    const [expandedModules, setExpandedModules] = useState([]);
    const [selectedLesson, setSelectedLesson] = useState(null);

    const [isEnrolled, setIsEnrolled] = useState(false);
    const [enrolling, setEnrolling] = useState(false);
    const [enrollmentMessage, setEnrollmentMessage] = useState("");

    // Load course, modules, lessons and enrollment information
    useEffect(() => {
        let isMounted = true;

        async function loadCourseData() {
            setLoading(true);
            setError("");
            setCurriculumError("");
            setSelectedLesson(null);

            try {
                const [courseData, moduleData, lessonData] =
                    await Promise.all([
                        getCourseById(courseId),
                        getModules(),
                        getLessons(),
                    ]);

                const allModules = Array.isArray(moduleData)
                    ? moduleData
                    : moduleData.results || [];

                const allLessons = Array.isArray(lessonData)
                    ? lessonData
                    : lessonData.results || [];

                const courseModules = allModules.filter(
                    (module) =>
                        String(module.course?.id ?? module.course) ===
                        String(courseId) &&
                        module.is_active !== false
                );

                const moduleIds = courseModules.map((module) =>
                    String(module.id)
                );

                const courseLessons = allLessons.filter(
                    (lesson) =>
                        moduleIds.includes(
                            String(lesson.module?.id ?? lesson.module)
                        ) &&
                        lesson.is_active !== false
                );

                if (!isMounted) return;

                setCourse(courseData);
                setModules(courseModules);
                setLessons(courseLessons);

                if (courseModules.length > 0) {
                    setExpandedModules([String(courseModules[0].id)]);
                }

                // Check whether the student is enrolled
                try {
                    const enrollmentData = await getMyEnrollments();

                    const enrollmentList = Array.isArray(enrollmentData)
                        ? enrollmentData
                        : enrollmentData.results || [];

                    const alreadyEnrolled = enrollmentList.some(
                        (enrollment) =>
                            String(
                                enrollment.course?.id ?? enrollment.course
                            ) === String(courseId) &&
                            enrollment.is_active !== false
                    );

                    if (isMounted) {
                        setIsEnrolled(alreadyEnrolled);
                    }
                } catch (enrollmentError) {
                    console.error(
                        "Failed to load enrollment status:",
                        enrollmentError
                    );
                }
            } catch (err) {
                console.error("Failed to load course:", err);

                if (isMounted) {
                    setError(
                        "Unable to load course details. Please try again."
                    );
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        }

        loadCourseData();

        return () => {
            isMounted = false;
        };
    }, [courseId]);

    // Expand or collapse a module
    const toggleModule = (moduleId) => {
        setExpandedModules((previous) =>
            previous.includes(String(moduleId))
                ? previous.filter((id) => id !== String(moduleId))
                : [...previous, String(moduleId)]
        );
    };

    // Enroll in course
    const handleEnroll = async () => {
        setEnrolling(true);
        setEnrollmentMessage("");

        try {
            await enrollInCourse(courseId);

            setIsEnrolled(true);
            setEnrollmentMessage(
                "You have successfully enrolled in this course!"
            );
        } catch (err) {
            console.error("Enrollment failed:", err);

            const message =
                err.course?.[0] ||
                err.course ||
                err.detail ||
                "Unable to enroll. Please try again.";

            setEnrollmentMessage(
                typeof message === "string"
                    ? message
                    : "Enrollment failed."
            );
        } finally {
            setEnrolling(false);
        }
    };

    // Get icon according to lesson type
    const getLessonIcon = (type) => {
        switch (type) {
            case "video":
                return <PlayCircle size={19} />;

            case "ppt":
                return <Presentation size={19} />;

            case "link":
                return <LinkIcon size={19} />;

            case "pdf":
            case "text":
            default:
                return <FileText size={19} />;
        }
    };

    // Get the lesson file URL
    const getLessonFileUrl = (lesson) => {
        const file = lesson?.file;

        if (typeof file === "string") {
            return file;
        }

        return file?.url || "";
    };


    const formatFileSize = (bytes) => {
        if (bytes == null || bytes < 0) return "";

        if (bytes < 1024 * 1024) {
            return `${(bytes / 1024).toFixed(1)} KB`;
        }

        return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    };


    // Display selected lesson content
    const renderLessonContent = () => {
        if (!selectedLesson) return null;

        const contentType = selectedLesson.content_type;
        const fileUrl = getLessonFileUrl(selectedLesson);

        return (
            <div className="lesson-content-viewer">
                <div className="lesson-content-header">
                    <span>NOW LEARNING</span>

                    <h2>{selectedLesson.title}</h2>

                    {selectedLesson.description && (
                        <p>{selectedLesson.description}</p>
                    )}

                    <span className="lesson-type-label">
                        {contentType?.toUpperCase()}
                    </span>


                    {["pdf", "ppt"].includes(contentType) && fileUrl && (
                        <div className="lesson-file-info">
                            <FileText size={18} />
                            <div>
                                <strong>
                                    {selectedLesson.file_name || "Lesson document"}
                                </strong>
                                <span>
                                    {formatFileSize(selectedLesson.file_size)}
                                </span>
                            </div>
                        </div>
                    )}

                </div>

                {/* TEXT LESSON */}
                {contentType === "text" && (
                    <div className="lesson-text-content">
                        {selectedLesson.text_content ? (
                            <div>
                                {selectedLesson.text_content}
                            </div>
                        ) : (
                            <p>
                                No text content is available for this lesson.
                            </p>
                        )}
                    </div>
                )}


                {/* VIDEO LESSON */}
                {contentType === "video" && (
                    fileUrl ? (
                        <div className="lesson-video-container">
                            <video
                                className="lesson-video"
                                controls
                                playsInline
                                preload="metadata"
                                key={fileUrl}
                            >
                                <source src={fileUrl} type="video/mp4" />
                                Your browser does not support video playback.
                            </video>
                        </div>
                    ) : (
                        <p className="lesson-content-message">
                            No video has been uploaded for this lesson.
                        </p>
                    )
                )}


                {/* PDF LESSON */}
                {contentType === "pdf" && (
                    fileUrl ? (
                        <iframe
                            className="lesson-pdf"
                            src={fileUrl}
                            title={selectedLesson.title}
                        />
                    ) : (
                        <p className="lesson-content-message">
                            No PDF has been uploaded for this lesson.
                        </p>
                    )
                )}

                {/* POWERPOINT LESSON */}
                {contentType === "ppt" && (
                    fileUrl ? (
                        <div className="lesson-file-link">
                            <Presentation size={24} />

                            <a
                                href={fileUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                Open or download presentation
                            </a>
                        </div>
                    ) : (
                        <p className="lesson-content-message">
                            No presentation has been uploaded.
                        </p>
                    )
                )}

                {/* EXTERNAL LINK LESSON */}
                {contentType === "link" && (
                    selectedLesson.external_link ? (
                        <div className="lesson-file-link">
                            <LinkIcon size={24} />

                            <a
                                href={selectedLesson.external_link}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                Open lesson link
                            </a>
                        </div>
                    ) : (
                        <p className="lesson-content-message">
                            No external link is available.
                        </p>
                    )
                )}

                {/* OTHER CONTENT TYPES */}
                {![
                    "text",
                    "video",
                    "pdf",
                    "ppt",
                    "link",
                ].includes(contentType) && (
                        <p className="lesson-content-message">
                            This lesson type is not supported in the viewer yet.
                        </p>
                    )}
            </div>
        );
    };

    if (loading) {
        return (
            <div className="course-details-status">
                Loading course details...
            </div>
        );
    }

    if (error || !course) {
        return (
            <div className="course-details-status">
                <p>{error || "Course not found."}</p>

                <button onClick={() => navigate("/dashboard")}>
                    Back to Dashboard
                </button>
            </div>
        );
    }

    return (
        <section className="course-details-page">

            {/* BACK BUTTON */}
            <button
                className="back-button"
                onClick={() => {
                    if (location.state?.from === "my-courses") {
                        navigate("/dashboard", {
                            state: { activeSection: "courses" },
                        });
                    } else {
                        navigate("/dashboard", {
                            state: { activeSection: "explore" },
                        });
                    }
                }}
            >
                <ArrowLeft size={18} />

                {location.state?.from === "my-courses"
                    ? "Back to My Courses"
                    : "Back to Explore Courses"}
            </button>

            {/* COURSE OVERVIEW */}
            <div className="course-details-header">
                <div className="course-details-info">

                    <span className="course-details-category">
                        {course.category || "General"}
                    </span>

                    <h1>{course.title}</h1>

                    <p>{course.description}</p>

                    <div className="course-details-meta">
                        <span>
                            <BookOpen size={17} />
                            {course.level || "All levels"}
                        </span>

                        <span>
                            <Clock size={17} />
                            {course.duration || "Self-paced"}
                        </span>

                        <span>
                            <BarChart3 size={17} />
                            Free Course
                        </span>
                    </div>

                    <button
                        className="enroll-button"
                        onClick={handleEnroll}
                        disabled={isEnrolled || enrolling}
                    >
                        {enrolling
                            ? "Enrolling..."
                            : isEnrolled
                                ? "Already Enrolled"
                                : "Enroll for Free"}
                    </button>

                    {enrollmentMessage && (
                        <p
                            className="enrollment-message"
                            role="status"
                        >
                            {enrollmentMessage}
                        </p>
                    )}
                </div>
            </div>

            {/* COURSE CURRICULUM */}
            <div className="course-curriculum">

                <div className="curriculum-heading">
                    <div>
                        <span>START LEARNING</span>

                        <h2>Course Curriculum</h2>

                        <p>
                            Explore the modules and lessons included in
                            this course.
                        </p>
                    </div>

                    <div className="curriculum-count">
                        <span>{modules.length} Modules</span>
                        <span>{lessons.length} Lessons</span>
                    </div>
                </div>

                {curriculumError && (
                    <p className="curriculum-error">
                        {curriculumError}
                    </p>
                )}

                {modules.length === 0 ? (
                    <div className="curriculum-empty">
                        <BookOpen size={35} />

                        <h3>Curriculum coming soon</h3>

                        <p>
                            Course modules and lessons haven't been
                            added yet.
                        </p>
                    </div>
                ) : (
                    <div className="curriculum-modules">

                        {modules.map((module, index) => {
                            const moduleId = String(module.id);

                            const moduleLessons = lessons.filter(
                                (lesson) =>
                                    String(
                                        lesson.module?.id ?? lesson.module
                                    ) === moduleId
                            );

                            const isExpanded =
                                expandedModules.includes(moduleId);

                            return (
                                <div
                                    className="curriculum-module"
                                    key={module.id}
                                >

                                    {/* MODULE HEADER */}
                                    <button
                                        type="button"
                                        className="module-header"
                                        onClick={() =>
                                            toggleModule(moduleId)
                                        }
                                    >
                                        <div className="module-title">

                                            <span className="module-number">
                                                {String(index + 1).padStart(
                                                    2,
                                                    "0"
                                                )}
                                            </span>

                                            <div>
                                                <h3>{module.title}</h3>

                                                <p>
                                                    {moduleLessons.length} Lessons
                                                </p>
                                            </div>
                                        </div>

                                        {isExpanded ? (
                                            <ChevronUp size={21} />
                                        ) : (
                                            <ChevronDown size={21} />
                                        )}
                                    </button>

                                    {/* MODULE LESSONS */}
                                    {isExpanded && (
                                        <div className="module-lessons">

                                            {module.description && (
                                                <p className="module-description">
                                                    {module.description}
                                                </p>
                                            )}

                                            {moduleLessons.length === 0 ? (
                                                <p className="no-lessons">
                                                    No lessons added yet.
                                                </p>
                                            ) : (
                                                moduleLessons.map((lesson) => {
                                                    const isSelected =
                                                        String(selectedLesson?.id) ===
                                                        String(lesson.id);

                                                    return (
                                                        <button
                                                            type="button"
                                                            className={`curriculum-lesson ${isSelected
                                                                ? "active"
                                                                : ""
                                                                }`}
                                                            key={lesson.id}
                                                            onClick={() =>
                                                                setSelectedLesson(
                                                                    lesson
                                                                )
                                                            }
                                                        >
                                                            <span className="lesson-icon">
                                                                {getLessonIcon(
                                                                    lesson.content_type
                                                                )}
                                                            </span>

                                                            <div className="lesson-info">
                                                                <h4>
                                                                    {lesson.title}
                                                                </h4>

                                                                <span>
                                                                    {lesson.content_type?.toUpperCase()}
                                                                </span>
                                                            </div>

                                                            {isSelected && (
                                                                <CheckCircle
                                                                    size={18}
                                                                    className="lesson-selected-icon"
                                                                />
                                                            )}
                                                        </button>
                                                    );
                                                })
                                            )}
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                )}

                {/* SELECTED LESSON CONTENT */}
                {renderLessonContent()}

            </div>
        </section>
    );
}

export default CourseDetails;
