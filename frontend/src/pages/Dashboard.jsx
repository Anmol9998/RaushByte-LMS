
import { Link } from "react-router-dom";
import { BookOpen, Bell, Award, UserRound, LogOut } from "lucide-react";
import "./Dashboard.css";
import { useNavigate } from "react-router-dom";

function Dashboard() {
    const navigate = useNavigate();
    const storedUser = JSON.parse(localStorage.getItem("user") || "{}");
    const user = storedUser.user || storedUser;

    const handleLogout = () => {
        localStorage.removeItem("user");
        navigate("/");
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
                        <h1>Welcome back, {user.first_name || user.username || "Learner"}!</h1>
                        <p>Ready to continue your learning journey?</p>
                    </div>
                    <button className="dashboard-notifications" aria-label="Notifications">
                        <Bell size={21} />
                    </button>
                </header>

                <section className="dashboard-welcome">
                    <div>
                        <span>YOUR LEARNING JOURNEY</span>
                        <h2>Learn something new today.</h2>
                        <p>Explore courses, develop your skills, and keep moving forward.</p>
                        <a href="#courses" className="dashboard-cta">Explore learning</a>
                    </div>
                    <BookOpen size={90} strokeWidth={1.2} />
                </section>

                <section className="dashboard-stats">
                    <article>
                        <BookOpen size={24} />
                        <h3>0</h3>
                        <p>Enrolled courses</p>
                    </article>
                    <article>
                        <Award size={24} />
                        <h3>0</h3>
                        <p>Certificates earned</p>
                    </article>
                    <article>
                        <UserRound size={24} />
                        <h3>Student</h3>
                        <p>Account role</p>
                    </article>
                </section>

                <section className="dashboard-courses" id="courses">
                    <div>
                        <h2>My Learning</h2>
                        <p>Your enrolled courses will appear here.</p>
                    </div>
                    <div className="dashboard-empty">
                        <BookOpen size={34} />
                        <h3>No courses yet</h3>
                        <p>Once courses are available, you can start learning here.</p>
                    </div>
                </section>
            </section>
        </main>
    );
}

export default Dashboard;
