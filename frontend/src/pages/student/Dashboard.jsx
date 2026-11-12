
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
    BookOpen,
    Bell,
    Award,
    UserRound,
    LogOut,
} from "lucide-react";

import { getCourses } from "../../services/modules/courses.service";
import "./Dashboard.css";

function Dashboard() {
    const navigate = useNavigate();

    const storedUser = JSON.parse(localStorage.getItem("user") || "{}");
    const user = storedUser.user || storedUser;

    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function fetchCourses() {
            try {
                setLoading(true);
                setError("");

                const data = await getCourses();

                // Supports both array and paginated API responses
                setCourses(Array.isArray(data) ? data : data.results || []);
            } catch (err) {
                console.error("Course fetching error:", err);
                setError("Unable to load courses. Please try again.");
            } finally {
                setLoading(false);
            }
        }

        fetchCourses();
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("user");
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");

        navigate("/login", { replace: true });
    };

    return (
        <main className="dashboard-page">
            <aside className="dashboard-sidebar">
                <Link to="/" className="dashboard-brand">
                    RaushByte <strong>Learn</strong>
                </Link>

                <nav className="dashboard-nav">
                    <a href="#overview" className="active">
                        <BookOpen size={19} /> Overview
                    </a>

                    <a href="#courses">
                        <BookOpen size={19} /> My Courses
                    </a>

                    <a href="#certificates">
                        <Award size={19} /> Certificates
                    </a>

                    <a href="#profile">
                        <UserRound size={19} /> My Profile
                    </a>
                </nav>

                <button className="dashboard-logout" onClick={handleLogout}>
                    <LogOut size={19} /> Log out
                </button>
            </aside>

            <section className="dashboard-main" id="overview">
                <header className="dashboard-header">
                    <div>
                        <p className="dashboard-eyebrow">STUDENT SPACE</p>

                        <h1>
                            Welcome back,{" "}
                            {user.first_name || user.username || "Learner"}!
                        </h1>

                        <p>Ready to continue your learning journey?</p>
                    </div>

                    <button
                        className="dashboard-notifications"
                        aria-label="Notifications"
                    >
                        <Bell size={21} />
                    </button>
                </header>

                <section className="dashboard-welcome">
                    <div>
                        <span>YOUR LEARNING JOURNEY</span>
                        <h2>Learn something new today.</h2>

                        <p>
                            Explore courses, develop your skills, and keep moving forward.
                        </p>

                        <a href="#courses" className="dashboard-cta">
                            Explore learning
                        </a>
                    </div>

                    <BookOpen size={90} strokeWidth={1.2} />
                </section>

                <section className="dashboard-stats">
                    <article>
                        <BookOpen size={24} />
                        <h3>{courses.length}</h3>
                        <p>Available courses</p>
                    </article>

                    <article>
                        <Award size={24} />
                        <h3>0</h3>
                        <p>Certificates earned</p>
                    </article>

                    <article>
                        <UserRound size={24} />
                        <h3>{user.role || "Student"}</h3>
                        <p>Account role</p>
                    </article>
                </section>

                <section className="dashboard-courses" id="courses">
                    <div>
                        <h2>Available Courses</h2>
                        <p>Explore courses and start learning.</p>
                    </div>

                    {loading ? (
                        <div className="dashboard-empty">
                            <p>Loading courses...</p>
                        </div>
                    ) : error ? (
                        <div className="dashboard-empty">
                            <p>{error}</p>
                            <button onClick={() => window.location.reload()}>
                                Try again
                            </button>
                        </div>
                    ) : courses.length === 0 ? (
                        <div className="dashboard-empty">
                            <BookOpen size={34} />
                            <h3>No courses available</h3>
                            <p>New courses will appear here when they are published.</p>
                        </div>
                    ) : (
                        <div className="dashboard-course-list">
                            {courses.map((course) => (
                                <article
                                    className="dashboard-course-card"
                                    key={course.id || course._id}
                                >
                                    <BookOpen size={28} />

                                    <h3>{course.title || course.name || "Untitled Course"}</h3>

                                    <p>
                                        {course.description || "Explore this course and start learning."}
                                    </p>
                                </article>
                            ))}
                        </div>
                    )}
                </section>
            </section>
        </main>
    );
}

export default Dashboard;

