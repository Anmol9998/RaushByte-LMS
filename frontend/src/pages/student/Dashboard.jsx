
import ExploreCourses from "./ExploreCourses";

import { getMyEnrollments } from "../../services/modules/enrollment.service";

import { useEffect, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

import CourseCard from "../../components/common/CourseCard";
import "../../components/home/FeaturedCourses.css";

import {
    BookOpen,
    Bell,
    Award,
    UserRound,
    LogOut,
} from "lucide-react";

import { useAuth } from "../../context/AuthContext";
import "./Dashboard.css";


function Dashboard() {
    const navigate = useNavigate();
    const { user, logout } = useAuth();

    const location = useLocation();

    const [activeSection, setActiveSection] = useState(
        location.state?.activeSection || "overview"
    );
    const [enrollments, setEnrollments] = useState([]);
    const [enrollmentLoading, setEnrollmentLoading] = useState(true);
    const [enrollmentError, setEnrollmentError] = useState("");


    // Fetch enrolled courses
    useEffect(() => {
        async function loadEnrollments() {
            try {
                setEnrollmentLoading(true);
                setEnrollmentError("");

                const data = await getMyEnrollments();

                const enrollmentList = Array.isArray(data)
                    ? data
                    : data.results || [];

                setEnrollments(
                    enrollmentList.filter(
                        (enrollment) => enrollment.is_active !== false
                    )
                );

            } catch (error) {
                console.error("Failed to load enrolled courses:", error);
                setEnrollmentError(
                    "Unable to load your enrolled courses."
                );
            } finally {
                setEnrollmentLoading(false);
            }
        }

        loadEnrollments();
    }, []);


    // Logout
    const handleLogout = () => {
        logout();
        navigate("/", { replace: true });
    };


    // Reusable enrolled course cards
    const renderMyCourses = () => {
        if (enrollmentLoading) {
            return (
                <div className="dashboard-empty">
                    Loading your courses...
                </div>
            );
        }

        if (enrollmentError) {
            return (
                <div className="dashboard-empty">
                    <p>{enrollmentError}</p>
                </div>
            );
        }

        if (enrollments.length === 0) {
            return (
                <div className="dashboard-empty">
                    <BookOpen size={34} />
                    <h3>No courses yet</h3>
                    <p>
                        Explore available courses and enroll to start learning.
                    </p>

                    <button
                        className="dashboard-cta"
                        onClick={() => setActiveSection("explore")}
                    >
                        Explore Courses
                    </button>
                </div>
            );
        }

        return (
            <div className="my-courses-grid">
                {enrollments.map((enrollment) => (
                    <article
                        className="course-card"
                        key={enrollment.id}
                    >
                        <CourseCard
                            course={{
                                title: enrollment.course_title,
                                description:
                                    "Continue learning and build your skills.",
                                category: "Enrolled Course",
                                level: "All levels",
                                duration: "Self-paced",
                                color: "blue",
                                icon: "📚",
                            }}
                            actionLabel="Continue Learning"
                            onAction={() =>
                                navigate(`/courses/${enrollment.course}`, {
                                    state: { from: "my-courses" },
                                })
                            }
                        />
                    </article>
                ))}
            </div>
        );
    };


    return (
        <main className="dashboard-page">

            {/* Sidebar */}
            <aside className="dashboard-sidebar">

                <Link to="/" className="dashboard-brand">
                    RaushByte <strong>Learn</strong>
                </Link>

                <nav className="dashboard-nav">

                    <a
                        href="#overview"
                        className={
                            activeSection === "overview" ? "active" : ""
                        }
                        onClick={() => setActiveSection("overview")}
                    >
                        <BookOpen size={19} />
                        Overview
                    </a>

                    <a
                        href="#explore"
                        className={
                            activeSection === "explore" ? "active" : ""
                        }
                        onClick={() => setActiveSection("explore")}
                    >
                        <BookOpen size={19} />
                        Explore Courses
                    </a>

                    <a
                        href="#courses"
                        className={
                            activeSection === "courses" ? "active" : ""
                        }
                        onClick={() => setActiveSection("courses")}
                    >
                        <BookOpen size={19} />
                        My Courses
                    </a>

                    <a
                        href="#certificates"
                        onClick={() => setActiveSection("certificates")}
                        className={
                            activeSection === "certificates" ? "active" : ""
                        }
                    >
                        <Award size={19} />
                        Certificates
                    </a>

                    <a
                        href="#profile"
                        onClick={() => setActiveSection("profile")}
                        className={
                            activeSection === "profile" ? "active" : ""
                        }
                    >
                        <UserRound size={19} />
                        My Profile
                    </a>

                </nav>

                <button
                    className="dashboard-logout"
                    onClick={handleLogout}
                >
                    <LogOut size={19} />
                    Log out
                </button>

            </aside>


            {/* Main Dashboard */}
            <section className="dashboard-main">

                {/* Explore Courses */}
                {activeSection === "explore" ? (
                    <ExploreCourses />
                ) : activeSection === "overview" ? (

                    <>
                        {/* Header */}
                        <header className="dashboard-header">

                            <div>
                                <p className="dashboard-eyebrow">
                                    STUDENT SPACE
                                </p>

                                <h1>
                                    Welcome back,{" "}
                                    {user?.first_name ||
                                        user?.username ||
                                        "Learner"}!
                                </h1>

                                <p>
                                    Ready to continue your learning journey?
                                </p>
                            </div>

                            <button
                                className="dashboard-notifications"
                                aria-label="Notifications"
                            >
                                <Bell size={21} />
                            </button>

                        </header>


                        {/* Welcome Section */}
                        <section className="dashboard-welcome">

                            <div>
                                <span>YOUR LEARNING JOURNEY</span>

                                <h2>Learn something new today.</h2>

                                <p>
                                    Explore courses, develop your skills,
                                    and keep moving forward.
                                </p>

                                <button
                                    className="dashboard-cta"
                                    onClick={() =>
                                        setActiveSection("explore")
                                    }
                                >
                                    Explore learning
                                </button>
                            </div>

                            <BookOpen
                                size={90}
                                strokeWidth={1.2}
                            />

                        </section>


                        {/* Dashboard Statistics */}
                        <section className="dashboard-stats">

                            <article>
                                <BookOpen size={24} />

                                <h3>
                                    {enrollmentLoading
                                        ? "..."
                                        : enrollments.length}
                                </h3>

                                <p>Enrolled courses</p>
                            </article>

                            <article>
                                <Award size={24} />

                                <h3>0</h3>

                                <p>Certificates earned</p>
                            </article>

                            <article>
                                <UserRound size={24} />

                                <h3>{user?.role || "Student"}</h3>

                                <p>Account role</p>
                            </article>

                        </section>


                        {/* My Learning Preview */}
                        <section
                            className="dashboard-courses"
                            id="courses"
                        >

                            <div>
                                <h2>My Learning</h2>

                                <p>
                                    Continue learning from your enrolled courses.
                                </p>
                            </div>

                            {renderMyCourses()}

                        </section>

                    </>

                ) : activeSection === "courses" ? (

                    /* My Courses */
                    <section
                        className="dashboard-courses"
                        id="courses"
                    >

                        <div>
                            <h2>My Courses</h2>

                            <p>
                                Continue learning from your enrolled courses.
                            </p>
                        </div>

                        {renderMyCourses()}

                    </section>

                ) : activeSection === "certificates" ? (

                    /* Certificates */
                    <section className="dashboard-courses">
                        <h2>My Certificates</h2>

                        <div className="dashboard-empty">
                            <Award size={34} />

                            <h3>No certificates yet</h3>

                            <p>
                                Your earned certificates will appear here.
                            </p>
                        </div>
                    </section>

                ) : activeSection === "profile" ? (

                    /* Profile */
                    <section className="dashboard-courses">
                        <h2>My Profile</h2>

                        <div className="dashboard-empty">
                            <UserRound size={34} />

                            <h3>
                                {user?.first_name || user?.username || "Student"}
                            </h3>

                            <p>{user?.email}</p>

                            <p>
                                Role: {user?.role || "Student"}
                            </p>
                        </div>
                    </section>

                ) : null}

            </section>

        </main>
    );
}

export default Dashboard;
