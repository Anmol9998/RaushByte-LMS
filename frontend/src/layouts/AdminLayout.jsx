
import { useState } from "react";
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
    Settings,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";

function AdminLayout({ children, activeSection, onSectionChange }) {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const [searchTerm, setSearchTerm] = useState("");

    const menuItems = [
        { id: "overview", label: "Overview", icon: LayoutDashboard },
        { id: "users", label: "User Management", icon: Users },
        { id: "courses", label: "Courses", icon: BookOpen },
        { id: "batches", label: "Internship Batches", icon: GraduationCap },
        { id: "assignments", label: "Assignments", icon: ClipboardList },
        { id: "certificates", label: "Certificates", icon: Award },
    ];

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    const sectionTitles = {
        overview: "Overview",
        users: "User Management",
        courses: "Course Management",
        batches: "Internship Batches",
        assignments: "Assignments",
        certificates: "Certificates",
    };

    return (
        <div className="admin-dashboard">
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
                                    onClick={() => onSectionChange(item.id)}
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

            <main className="admin-main">
                <header className="admin-topbar">
                    <div className="admin-breadcrumb">
                        <span>Admin</span>
                        <span className="breadcrumb-divider">/</span>
                        <strong>
                            {sectionTitles[activeSection] || "Overview"}
                        </strong>
                    </div>

                    <div className="admin-topbar-right">
                        <div className="admin-search">
                            <Search size={17} />
                            <input
                                type="text"
                                placeholder="Search..."
                                aria-label="Search"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
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
                                {(user?.first_name || user?.username || "A")
                                    .charAt(0)
                                    .toUpperCase()}
                            </div>

                            <div className="admin-profile-info">
                                <strong>
                                    {user?.first_name || user?.username || "Admin"}
                                </strong>
                                <span>Administrator</span>
                            </div>
                        </div>
                    </div>
                </header>

                <section className="admin-content">
                    {children}
                </section>
            </main>
        </div>
    );
}

export default AdminLayout;
