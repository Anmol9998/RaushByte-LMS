function CourseCard({ course, actionLabel = "Explore Course", onAction }) {
    return (
        <>
            <div className={`course-visual ${course.color || "blue"}`}>
                <span className="course-icon">
                    {course.icon || "{"}
                </span>
                <span className="course-category">
                    {course.category || "General"}
                </span>
            </div>

            <div className="course-content">
                <div className="course-meta">
                    <span>{course.level || "All levels"}</span>
                    <span>{course.duration || "Self-paced"}</span>
                </div>

                <h3>{course.title}</h3>
                <p>{course.description}</p>

                <button
                    type="button"
                    className="course-link"
                    onClick={() => onAction?.(course)}
                >
                    {actionLabel}
                    <span aria-hidden="true">→</span>
                </button>
            </div>
        </>
    );
}

export default CourseCard;