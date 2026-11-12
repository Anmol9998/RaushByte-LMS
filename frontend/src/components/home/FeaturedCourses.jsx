
import { useRef, useState } from "react";
import { motion } from "motion/react";
import "./FeaturedCourses.css";

const courses = [
    {
        id: 1,
        category: "Web Development",
        title: "Frontend Development",
        description:
            "Learn HTML, CSS, JavaScript, and React by building interactive websites.",
        level: "Beginner",
        duration: "8 weeks",
        color: "blue",
        icon: "</>",
    },
    {
        id: 2,
        category: "Programming",
        title: "Python Programming",
        description:
            "Build a strong programming foundation and learn to solve problems with Python.",
        level: "Beginner",
        duration: "6 weeks",
        color: "orange",
        icon: "Py",
    },
    {
        id: 3,
        category: "Backend Development",
        title: "Backend with Django",
        description:
            "Explore Python web development, REST APIs, and database integration.",
        level: "Intermediate",
        duration: "8 weeks",
        color: "green",
        icon: "Dj",
    },
    {
        id: 4,
        category: "C++ Development",
        title: "C++ Programming",
        description:
            "Learn object-oriented programming, data structures, and problem-solving with C++.",
        level: "Beginner",
        duration: "8 weeks",
        color: "blue",
        icon: "C++",
    },
];

function FeaturedCourses() {
    const carouselRef = useRef(null);
    const isDragging = useRef(false);
    const startX = useRef(0);
    const startScrollLeft = useRef(0);
    const dragDistance = useRef(0);

    const [isDraggingNow, setIsDraggingNow] = useState(false);

    const handlePointerDown = (e) => {
        if (e.pointerType !== "mouse" || e.button !== 0) return;

        const carousel = carouselRef.current;
        if (!carousel) return;

        isDragging.current = true;
        dragDistance.current = 0;
        startX.current = e.clientX;
        startScrollLeft.current = carousel.scrollLeft;

        setIsDraggingNow(true);
        e.currentTarget.setPointerCapture(e.pointerId);
    };

    const handlePointerMove = (e) => {
        if (!isDragging.current || !carouselRef.current) return;

        const distance = e.clientX - startX.current;
        dragDistance.current = Math.abs(distance);

        carouselRef.current.scrollLeft =
            startScrollLeft.current - distance;
    };

    const handlePointerUp = () => {
        isDragging.current = false;
        setIsDraggingNow(false);
    };

    const handleClickCapture = (e) => {
        if (dragDistance.current > 5) {
            e.preventDefault();
            e.stopPropagation();
        }

        dragDistance.current = 0;
    };

    return (
        <section className="courses-section" id="courses">
            <div className="courses-container">
                <motion.div
                    className="courses-heading"
                    initial={{ opacity: 0, y: 25 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, amount: 0.2 }}
                    transition={{ duration: 0.6 }}
                >
                    <div>
                        <span className="section-label">
                            START LEARNING
                        </span>

                        <h2>
                            Explore our <span>courses</span>
                        </h2>

                        <p>
                            Build practical skills, learn new technologies,
                            and take the next step in your learning journey.
                        </p>
                    </div>

                    <a
                        href="#all-courses"
                        className="view-courses-link"
                    >
                        View all courses <span aria-hidden="true">&rarr;</span>
                    </a>
                </motion.div>

                <div className="courses-carousel-wrapper">
                    <div
                        className={`courses-grid ${isDraggingNow ? "is-dragging" : ""
                            }`}
                        ref={carouselRef}
                        onPointerDown={handlePointerDown}
                        onPointerMove={handlePointerMove}
                        onPointerUp={handlePointerUp}
                        onPointerCancel={handlePointerUp}
                        onClickCapture={handleClickCapture}
                        aria-label="Available courses"
                    >
                        {courses.map((course, index) => (
                            <motion.article
                                className="course-card"
                                key={course.id}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true, amount: 0.15 }}
                                transition={{
                                    duration: 0.45,
                                    delay: index * 0.12,
                                }}
                                whileHover={
                                    isDraggingNow ? {} : { y: -6 }
                                }
                            >
                                <div
                                    className={`course-visual ${course.color}`}
                                >
                                    <span className="course-icon">
                                        {course.icon}
                                    </span>

                                    <span className="course-category">
                                        {course.category}
                                    </span>
                                </div>

                                <div className="course-content">
                                    <div className="course-meta">
                                        <span>{course.level}</span>
                                        <span>{course.duration}</span>
                                    </div>

                                    <h3>{course.title}</h3>

                                    <p>{course.description}</p>

                                    <a
                                        href="#login"
                                        className="course-link"
                                        aria-label={`Explore ${course.title}`}
                                    >
                                        Explore course{" "}
                                        <span aria-hidden="true">&rarr;</span>
                                    </a>
                                </div>
                            </motion.article>
                        ))}
                    </div>
                </div>

                <p className="courses-note">
                    Course details shown here are sample content and will be
                    replaced with information from the backend.
                </p>
            </div>
        </section>
    );
}

export default FeaturedCourses;
