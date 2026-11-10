
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
    LayoutDashboard,
    Users,
    BookOpen,
    GraduationCap,
    ClipboardList,
    Award,
    Bell,
    Search,
    LogOut,
    Plus,
    ArrowUpRight,
    CalendarDays,
    Settings,
    UserCheck,
} from "lucide-react";

import UserManagement from "./UserManagement";
import CourseManagement from "./CourseManagement";

import { getDashboardSummary } from "../services/api";

import "./AdminDashboard.css";

function AdminDashboard() {
    const navigate = useNavigate();

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

    const user = JSON.parse(localStorage.getItem("user") || "{}");

    const isAdmin =
        user.is_admin ||
        user.is_staff ||
        user.is_superuser ||
        user.role === "admin";

    // Load dashboard statistics
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

    // Check admin access
    useEffect(() => {
        if (!isAdmin) {
            navigate("/dashboard", { replace: true });
            return;
        }

        loadDashboard();
    }, []);

    // Logout
    const handleLogout = () => {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("user");

        navigate("/login");
    };

    // Dashboard statistics
    const stats = [
        {
            label: "Total Students",
            value: summary.total_students,
            icon: Users,
            color: "blue",
        },
        {
            label: "Total Mentors",
            value: summary.total_mentors,
            icon: GraduationCap,
            color: "orange",
        },
        {
            label: "Total Admins",
            value: summary.total_admins,
            icon: UserCheck,
            color: "green",
        },
        {
            label: "Active Courses",
            value: summary.active_courses,
            icon: BookOpen,
            color: "purple",
        },
        {
            label: "Internship Batches",
            value: summary.internship_batches,
            icon: ClipboardList,
            color: "green",
        },
    ];

    // Sidebar menu items
    const menuItems = [
        {
            id: "overview",
            label: "Overview",
            icon: LayoutDashboard,
        },
        {
            id: "users",
            label: "User Management",
            icon: Users,
        },
        {
            id: "courses",
            label: "Courses",
            icon: BookOpen,
        },
        {
            id: "batches",
            label: "Internship Batches",
            icon: GraduationCap,
        },
        {
            id: "assignments",
            label: "Assignments",
            icon: ClipboardList,
        },
        {
            id: "certificates",
            label: "Certificates",
            icon: Award,
        },
    ];

    // Handle sidebar navigation
    const handleMenuClick = (section) => {
        if (["overview", "users", "courses"].includes(section)) {
            setActiveSection(section);
        } else {
            alert(`${section} section is coming soon.`);
        }
    };

    // Breadcrumb title
    const getSectionTitle = () => {
        const titles = {
            overview: "Overview",
            users: "User Management",
            courses: "Course Management",
            batches: "Internship Batches",
            assignments: "Assignments",
            certificates: "Certificates",
        };

        return titles[activeSection] || "Overview";
    };

    return (
        <div className="admin-dashboard">

            {/* Sidebar */}
            <aside className="admin-sidebar">

                <div className="admin-logo">
                    <Link to="/">
                        <span className="logo-text">
                            Raush<span>Byte</span>
                        </span>
                    </Link>

                    <p>ADMIN PANEL</p>
                </div>

                <div className="admin-sidebar-section">
                    <p className="sidebar-heading">MAIN MENU</p>

                    <nav className="admin-nav">
                        {menuItems.map((item) => {
                            const Icon = item.icon;

                            return (
                                <button
                                    key={item.id}
                                    className={`admin-nav-item ${activeSection === item.id ? "active" : ""
                                        }`}
                                    onClick={() => handleMenuClick(item.id)}
                                >
                                    <Icon size={19} />
                                    <span>{item.label}</span>
                                </button>
                            );
                        })}
                    </nav>
                </div>

                <div className="admin-sidebar-bottom">

                    <button
                        className="admin-nav-item"
                        onClick={() => alert("Settings coming soon.")}
                    >
                        <Settings size={19} />
                        <span>Settings</span>
                    </button>

                    <button
                        className="admin-nav-item logout-item"
                        onClick={handleLogout}
                    >
                        <LogOut size={19} />
                        <span>Logout</span>
                    </button>

                </div>
            </aside>

            {/* Main Content */}
            <main className="admin-main">

                {/* Topbar */}
                <header className="admin-topbar">

                    <div className="admin-breadcrumb">
                        <span>Admin</span>
                        <span className="breadcrumb-divider">/</span>
                        <strong>{getSectionTitle()}</strong>
                    </div>

                    <div className="admin-topbar-right">

                        <div className="admin-search">
                            <Search size={17} />
                            <input
                                type="text"
                                placeholder="Search..."
                                aria-label="Search"
                            />
                        </div>

                        <button
                            className="admin-icon-button"
                            aria-label="Notifications"
                            onClick={() => alert("Notifications coming soon.")}
                        >
                            <Bell size={19} />
                        </button>

                        <div className="admin-profile">

                            <div className="admin-avatar">
                                {(user.first_name || user.username || "A")
                                    .charAt(0)
                                    .toUpperCase()}
                            </div>

                            <div className="admin-profile-info">
                                <strong>
                                    {user.first_name || user.username || "Admin"}
                                </strong>
                                <span>Administrator</span>
                            </div>

                        </div>
                    </div>
                </header>

                {/* Dashboard Content */}
                <section className="admin-content">

                    {/* User Management */}
                    {activeSection === "users" && (
                        <UserManagement />
                    )}

                    {/* Course Management */}
                    {activeSection === "courses" && (
                        <CourseManagement />
                    )}

                    {/* Dashboard Overview */}
                    {activeSection === "overview" && (
                        <>

                            {/* Overview Heading */}
                            <div className="admin-page-heading">

                                <div>
                                    <p className="admin-eyebrow">
                                        ADMINISTRATION
                                    </p>

                                    <h1>Dashboard Overview</h1>

                                    <p>
                                        Welcome back! Here's what's happening with your LMS.
                                    </p>
                                </div>

                                <button
                                    className="admin-primary-button"
                                    onClick={() => setActiveSection("users")}
                                >
                                    <Plus size={18} />
                                    Add a User
                                </button>

                            </div>

                            {/* Hero Section */}
                            <section className="admin-hero">

                                <div className="admin-hero-content">

                                    <span className="admin-hero-label">
                                        LEARNING MANAGEMENT SYSTEM
                                    </span>

                                    <h2>
                                        Manage your
                                        <span> learning ecosystem.</span>
                                    </h2>

                                    <p>
                                        Manage students, mentors, courses and internship
                                        batches from one place.
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

                            {/* Statistics */}
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
                                    <p className="admin-error-message">
                                        {error}
                                    </p>
                                )}

                                <div className="admin-stats-grid">

                                    {stats.map((stat) => {
                                        const Icon = stat.icon;

                                        return (
                                            <div
                                                className="admin-stat-card"
                                                key={stat.label}
                                            >

                                                <div className="admin-stat-top">

                                                    <div className={`admin-stat-icon ${stat.color}`}>
                                                        <Icon size={21} />
                                                    </div>

                                                    <ArrowUpRight
                                                        size={17}
                                                        className="admin-stat-arrow"
                                                    />

                                                </div>

                                                <h3>
                                                    {loading ? "..." : stat.value}
                                                </h3>

                                                <p>{stat.label}</p>

                                                <span className="admin-stat-note">
                                                    Live data
                                                </span>

                                            </div>
                                        );
                                    })}

                                </div>
                            </section>

                            {/* Lower Dashboard Panels */}
                            <section className="admin-lower-grid">

                                <div className="admin-panel">

                                    <div className="admin-panel-heading">
                                        <div>
                                            <h2>Quick Actions</h2>
                                            <p>Manage your platform</p>
                                        </div>
                                    </div>

                                    <div className="admin-quick-actions">

                                        {/* Manage Users */}
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

                                        {/* Manage Courses */}
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

                                        {/* Internship Batches */}
                                        <button
                                            className="admin-quick-action"
                                            onClick={() => handleMenuClick("batches")}
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

                                {/* Platform Updates */}
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

                            {/* Footer */}
                            <footer className="admin-footer">
                                <p>
                                    © {new Date().getFullYear()} RaushByte Learn.
                                    All rights reserved.
                                </p>

                                <span>Admin Dashboard</span>
                            </footer>

                        </>
                    )}

                </section>
            </main>
        </div>
    );
}

export default AdminDashboard;
