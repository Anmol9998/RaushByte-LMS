
import { useEffect, useState } from "react";
import { Plus, ArrowUpRight, CalendarDays, Bell, Users, GraduationCap, UserCheck, BookOpen, ClipboardList } from "lucide-react";

import AdminLayout from "../../layouts/AdminLayout";
import UserManagement from "./UserManagement";
import CourseManagement from "./CourseManagement";
import { getDashboardSummary } from "../../services/modules/admin.service";

import "./AdminDashboard.css";

function AdminDashboard() {
    const [activeSection, setActiveSection] = useState("overview");

    const [summary, setSummary] = useState({
        total_students: 0,
        total_mentors: 0,
        total_admins: 0,
        active_courses: 0,
        internship_batches: 0,
    });

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadDashboard = async () => {
        try {
            setLoading(true);
            setError("");

            const data = await getDashboardSummary();

            setSummary({
                total_students: data.total_students ?? 0,
                total_mentors: data.total_mentors ?? 0,
                total_admins: data.total_admins ?? 0,
                active_courses: data.active_courses ?? 0,
                internship_batches: data.internship_batches ?? 0,
            });
        } catch (err) {
            console.error("Dashboard loading error:", err);
            setError("Unable to load dashboard statistics.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadDashboard();
    }, []);

    const stats = [
        { label: "Total Students", value: summary.total_students, icon: Users, color: "blue" },
        { label: "Total Mentors", value: summary.total_mentors, icon: GraduationCap, color: "orange" },
        { label: "Total Admins", value: summary.total_admins, icon: UserCheck, color: "green" },
        { label: "Active Courses", value: summary.active_courses, icon: BookOpen, color: "purple" },
        { label: "Internship Batches", value: summary.internship_batches, icon: ClipboardList, color: "green" },
    ];

    return (
        <AdminLayout
            activeSection={activeSection}
            onSectionChange={setActiveSection}
        >
            {activeSection === "overview" && (
                <>
                    <div className="admin-page-heading">
                        <div>
                            <p className="admin-eyebrow">ADMINISTRATION</p>
                            <h1>Dashboard Overview</h1>
                            <p>Welcome back! Here's what's happening with your LMS.</p>
                        </div>

                        <button
                            className="admin-primary-button"
                            onClick={() => setActiveSection("users")}
                        >
                            <Plus size={18} />
                            Add a User
                        </button>
                    </div>

                    <section className="admin-hero">
                        <div className="admin-hero-content">
                            <span className="admin-hero-label">
                                LEARNING MANAGEMENT SYSTEM
                            </span>

                            <h2>
                                Manage your <span>learning ecosystem.</span>
                            </h2>

                            <p>
                                Manage students, mentors, courses and internship batches
                                from one place.
                            </p>

                            <button
                                className="admin-hero-button"
                                onClick={() => setActiveSection("users")}
                            >
                                Manage Users
                                <ArrowUpRight size={17} />
                            </button>
                        </div>

                        <div className="admin-hero-artwork">
                            <div className="admin-hero-circle">
                                <GraduationCap size={100} />
                            </div>
                        </div>
                    </section>

                    <section className="admin-stats-section">
                        <div className="admin-section-heading">
                            <div>
                                <h2>Platform Statistics</h2>
                                <p>Overview of your LMS performance</p>
                            </div>

                            <button
                                className="admin-refresh-button"
                                onClick={loadDashboard}
                                disabled={loading}
                            >
                                <ArrowUpRight size={16} />
                                Refresh
                            </button>
                        </div>

                        {error && (
                            <p className="admin-error-message">{error}</p>
                        )}

                        <div className="admin-stats-grid">
                            {stats.map((stat) => {
                                const Icon = stat.icon;

                                return (
                                    <div className="admin-stat-card" key={stat.label}>
                                        <div className="admin-stat-top">
                                            <div className={`admin-stat-icon ${stat.color}`}>
                                                <Icon size={21} />
                                            </div>
                                            <ArrowUpRight
                                                size={17}
                                                className="admin-stat-arrow"
                                            />
                                        </div>

                                        <h3>{loading ? "..." : stat.value}</h3>
                                        <p>{stat.label}</p>
                                        <span className="admin-stat-note">Live data</span>
                                    </div>
                                );
                            })}
                        </div>
                    </section>

                    <section className="admin-lower-grid">
                        <div className="admin-panel">
                            <div className="admin-panel-heading">
                                <div>
                                    <h2>Quick Actions</h2>
                                    <p>Manage your platform</p>
                                </div>
                            </div>

                            <div className="admin-quick-actions">
                                <button
                                    className="admin-quick-action"
                                    onClick={() => setActiveSection("users")}
                                >
                                    <div className="quick-action-icon">
                                        <Users size={20} />
                                    </div>
                                    <span>
                                        <strong>Manage Users</strong>
                                        <small>Add, edit or remove users</small>
                                    </span>
                                    <ArrowUpRight size={17} />
                                </button>

                                <button
                                    className="admin-quick-action"
                                    onClick={() => setActiveSection("courses")}
                                >
                                    <div className="quick-action-icon">
                                        <BookOpen size={20} />
                                    </div>
                                    <span>
                                        <strong>Manage Courses</strong>
                                        <small>Organize learning content</small>
                                    </span>
                                    <ArrowUpRight size={17} />
                                </button>

                                <button
                                    className="admin-quick-action"
                                    onClick={() => setActiveSection("batches")}
                                >
                                    <div className="quick-action-icon">
                                        <GraduationCap size={20} />
                                    </div>
                                    <span>
                                        <strong>Internship Batches</strong>
                                        <small>Manage internship programs</small>
                                    </span>
                                    <ArrowUpRight size={17} />
                                </button>
                            </div>
                        </div>

                        <div className="admin-panel">
                            <div className="admin-panel-heading">
                                <div>
                                    <h2>Platform Updates</h2>
                                    <p>Stay on top of your LMS</p>
                                </div>
                                <CalendarDays size={20} />
                            </div>

                            <div className="admin-update-empty">
                                <div className="admin-update-icon">
                                    <Bell size={23} />
                                </div>
                                <h3>You're all caught up!</h3>
                                <p>
                                    New platform updates and activities will appear here.
                                </p>
                            </div>
                        </div>
                    </section>

                    <footer className="admin-footer">
                        <p>
                            © {new Date().getFullYear()} RaushByte Learn.
                            All rights reserved.
                        </p>
                        <span>Admin Dashboard</span>
                    </footer>
                </>
            )}

            {activeSection === "users" && <UserManagement />}

            {activeSection === "courses" && <CourseManagement />}

            {["batches", "assignments", "certificates"].includes(activeSection) && (
                <div className="admin-page-heading">
                    <div>
                        <p className="admin-eyebrow">ADMINISTRATION</p>
                        <h1>
                            {activeSection.charAt(0).toUpperCase() +
                                activeSection.slice(1)}
                        </h1>
                        <p>This section is coming soon.</p>
                    </div>
                </div>
            )}
        </AdminLayout>
    );
}

export default AdminDashboard;
