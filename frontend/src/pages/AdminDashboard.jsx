
import { useEffect } from "react";
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
} from "lucide-react";
import "./AdminDashboard.css";

function AdminDashboard() {
    const navigate = useNavigate();

    const storedData = JSON.parse(localStorage.getItem("user") || "{}");
    const user = storedData.user || storedData;
    const isAdmin =
        user.is_admin ||
        user.is_staff ||
        user.is_superuser ||
        user.role === "admin";

    useEffect(() => {
        if (!storedData.access || !isAdmin) {
            navigate("/login", { replace: true });
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("user");
        navigate("/login", { replace: true });
    };

    const stats = [
        { label: "Total Students", value: "—", icon: Users, color: "blue" },
        { label: "Total Mentors", value: "—", icon: GraduationCap, color: "orange" },
        { label: "Active Courses", value: "—", icon: BookOpen, color: "purple" },
        { label: "Internship Batches", value: "—", icon: ClipboardList, color: "green" },
    ];

    const menuItems = [
        { label: "Overview", icon: LayoutDashboard, active: true },
        { label: "User Management", icon: Users },
        { label: "Courses", icon: BookOpen },
        { label: "Internship Batches", icon: GraduationCap },
        { label: "Assignments", icon: ClipboardList },
        { label: "Certificates", icon: Award },
    ];

    return (
        <div className="admin-layout">
            <aside className="admin-sidebar">
                <Link to="/" className="admin-brand">
                    <span className="admin-brand-icon"><BookOpen size={23} /></span>
                    <span>RaushByte <strong>Learn</strong></span>
                </Link>

                <div className="admin-sidebar-label">WORKSPACE</div>

                <nav className="admin-nav">
                    {menuItems.map(({ label, icon: Icon, active }) => (
                        <button
                            type="button"
                            key={label}
                            className={`admin-nav-item ${active ? "active" : ""}`}
                            onClick={() => {
                                if (!active) {
                                    alert(`${label} section will be connected next.`);
                                }
                            }}
                        >
                            <Icon size={19} />
                            <span>{label}</span>
                            {active && <span className="admin-active-indicator" />}
                        </button>
                    ))}
                </nav>

                <div className="admin-sidebar-bottom">
                    <button
                        type="button"
                        className="admin-nav-item"
                        onClick={() => alert("Settings will be added later.")}
                    >
                        <Settings size={19} />
                        <span>Settings</span>
                    </button>
                    <button
                        type="button"
                        className="admin-nav-item admin-logout"
                        onClick={handleLogout}
                    >
                        <LogOut size={19} />
                        <span>Log out</span>
                    </button>
                    <div className="admin-profile">
                        <div className="admin-avatar">
                            {(user.first_name || user.username || "A").charAt(0).toUpperCase()}
                        </div>
                        <div className="admin-profile-info">
                            <strong>
                                {user.first_name || user.username || "Administrator"}
                            </strong>
                            <span>Administrator</span>
                        </div>
                    </div>
                </div>
            </aside>

            <main className="admin-main">
                <header className="admin-topbar">
                    <div className="admin-breadcrumb">
                        <span>Workspace</span>
                        <span>/</span>
                        <strong>Overview</strong>
                    </div>

                    <div className="admin-topbar-actions">
                        <label className="admin-search">
                            <Search size={18} />
                            <input type="search" placeholder="Search dashboard..." />
                        </label>
                        <button
                            type="button"
                            className="admin-icon-button"
                            aria-label="Notifications"
                            onClick={() => alert("Notifications will be connected later.")}
                        >
                            <Bell size={20} />
                            <span />
                        </button>
                    </div>
                </header>

                <section className="admin-content">
                    <div className="admin-welcome-row">
                        <div>
                            <p className="admin-eyebrow">ADMINISTRATION</p>
                            <h1>Dashboard overview</h1>
                            <p className="admin-subtitle">
                                Welcome back, {user.first_name || user.username || "Admin"}.
                                Here's your learning platform at a glance.
                            </p>
                        </div>
                        <div className="admin-date">
                            <CalendarDays size={17} />
                            <span>{new Date().toLocaleDateString("en-IN", {
                                day: "numeric",
                                month: "short",
                                year: "numeric",
                            })}</span>
                        </div>
                    </div>

                    <section className="admin-hero">
                        <div className="admin-hero-content">
                            <span className="admin-hero-tag">RAUSHBYTE LEARN</span>
                            <h2>Build a better learning experience.</h2>
                            <p>
                                Manage learners, organize courses, and keep your training
                                programs moving forward from one place.
                            </p>
                            <button
                                type="button"
                                className="admin-primary-button"
                                onClick={() => alert("User management will be connected next.")}
                            >
                                <Plus size={18} /> Manage users
                            </button>
                        </div>
                        <div className="admin-hero-art">
                            <div className="admin-art-circle">
                                <GraduationCap size={76} strokeWidth={1.4} />
                            </div>
                            <span className="admin-art-dot dot-one" />
                            <span className="admin-art-dot dot-two" />
                        </div>
                    </section>

                    <div className="admin-section-heading">
                        <div>
                            <h2>Platform summary</h2>
                            <p>Your platform metrics will appear here.</p>
                        </div>
                    </div>

                    <section className="admin-stats-grid">
                        {stats.map(({ label, value, icon: Icon, color }) => (
                            <article className="admin-stat-card" key={label}>
                                <div className={`admin-stat-icon ${color}`}>
                                    <Icon size={22} />
                                </div>
                                <p>{label}</p>
                                <div className="admin-stat-bottom">
                                    <h3>{value}</h3>
                                    <span className="admin-stat-note">Awaiting API</span>
                                </div>
                            </article>
                        ))}
                    </section>

                    <section className="admin-lower-grid">
                        <article className="admin-panel admin-quick-panel">
                            <div className="admin-panel-heading">
                                <div>
                                    <h2>Quick actions</h2>
                                    <p>Common administration tasks</p>
                                </div>
                            </div>

                            <button
                                type="button"
                                className="admin-action-row"
                                onClick={() => alert("User creation will be connected next.")}
                            >
                                <span className="admin-action-icon orange"><Users size={20} /></span>
                                <span><strong>Add a user</strong><small>Create a student or mentor account</small></span>
                                <ArrowUpRight size={18} />
                            </button>

                            <button
                                type="button"
                                className="admin-action-row"
                                onClick={() => alert("Course creation will be connected next.")}
                            >
                                <span className="admin-action-icon blue"><BookOpen size={20} /></span>
                                <span><strong>Create a course</strong><small>Prepare new learning content</small></span>
                                <ArrowUpRight size={18} />
                            </button>

                            <button
                                type="button"
                                className="admin-action-row"
                                onClick={() => alert("Batch management will be connected next.")}
                            >
                                <span className="admin-action-icon purple"><GraduationCap size={20} /></span>
                                <span><strong>Set up an internship batch</strong><small>Organize learners into a batch</small></span>
                                <ArrowUpRight size={18} />
                            </button>
                        </article>

                        <article className="admin-panel admin-activity-panel">
                            <div className="admin-panel-heading">
                                <div>
                                    <h2>Recent activity</h2>
                                    <p>Latest platform updates</p>
                                </div>
                            </div>
                            <div className="admin-empty-activity">
                                <div><CalendarDays size={25} /></div>
                                <h3>No activity to show yet</h3>
                                <p>
                                    Recent registrations and platform updates will appear here
                                    when activity tracking is connected.
                                </p>
                            </div>
                        </article>
                    </section>

                    <footer className="admin-footer">
                        <span>© {new Date().getFullYear()} RaushByte Learn</span>
                        <span>Learn. Build. Grow.</span>
                    </footer>
                </section>
            </main>
        </div>
    );
}

export default AdminDashboard;
