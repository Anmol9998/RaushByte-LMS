
import { useEffect, useMemo, useState } from "react";
import {
    Search,
    Plus,
    Pencil,
    Trash2,
    X,
    Users,
    RefreshCw,
    UserCheck,
} from "lucide-react";

import {
    getUsers,
    createUser,
    updateUser,
    deleteUser,
} from "../services/api";

import "./UserManagement.css";

const emptyForm = {
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    role: "student",
};

function UserManagement() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [search, setSearch] = useState("");
    const [roleFilter, setRoleFilter] = useState("all");

    const [showModal, setShowModal] = useState(false);
    const [editingUser, setEditingUser] = useState(null);
    const [form, setForm] = useState(emptyForm);

    async function loadUsers() {
        try {
            setLoading(true);
            setError("");

            const data = await getUsers();
            setUsers(Array.isArray(data) ? data : data.results || []);
        } catch (err) {
            console.error("Users API error:", err);
            setError(
                err.detail ||
                "Unable to load users. Please check your connection and permissions."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadUsers();
    }, []);

    const filteredUsers = useMemo(() => {
        return users.filter((user) => {
            const searchText = search.toLowerCase();

            const matchesSearch = [
                user.first_name,
                user.last_name,
                user.username,
                user.email,
            ].some((value) =>
                (value || "").toLowerCase().includes(searchText)
            );

            const matchesRole =
                roleFilter === "all" || user.role === roleFilter;

            return matchesSearch && matchesRole;
        });
    }, [users, search, roleFilter]);

    function openAddModal() {
        setEditingUser(null);
        setForm(emptyForm);
        setError("");
        setShowModal(true);
    }

    function openEditModal(user) {
        setEditingUser(user);
        setForm({
            first_name: user.first_name || "",
            last_name: user.last_name || "",
            username: user.username || "",
            email: user.email || "",
            password: "",
            role: user.role || "student",
        });
        setError("");
        setShowModal(true);
    }

    function closeModal() {
        setShowModal(false);
        setEditingUser(null);
        setForm(emptyForm);
        setError("");
    }

    function handleChange(event) {
        const { name, value } = event.target;

        setForm((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            setSaving(true);
            setError("");

            const userData = {
                first_name: form.first_name.trim(),
                last_name: form.last_name.trim(),
                username: form.username.trim(),
                email: form.email.trim(),
                role: form.role,
            };

            if (editingUser) {
                await updateUser(editingUser.id, userData);
            } else {
                await createUser({
                    ...userData,
                    password: form.password,
                });
            }

            closeModal();
            await loadUsers();
        } catch (err) {
            console.error("Save user error:", err);

            const messages = Object.entries(err)
                .map(([field, value]) =>
                    `${field}: ${Array.isArray(value) ? value.join(", ") : value}`
                )
                .join("\n");

            setError(messages || "Unable to save user. Please try again.");
        } finally {
            setSaving(false);
        }
    }

    async function handleStatusChange(user) {
        const action = user.is_active ? "deactivate" : "activate";

        if (!window.confirm(`Are you sure you want to ${action} this account?`)) {
            return;
        }

        try {
            setError("");

            await updateUser(user.id, {
                is_active: !user.is_active,
            });

            await loadUsers();
        } catch (err) {
            console.error("Status update error:", err);
            setError("Unable to update account status.");
        }
    }

    async function handleDelete(user) {
        if (
            !window.confirm(
                `Are you sure you want to delete ${user.username}? This action cannot be undone.`
            )
        ) {
            return;
        }

        try {
            setError("");

            await deleteUser(user.id);
            await loadUsers();
        } catch (err) {
            console.error("Delete user error:", err);
            setError("Unable to delete this user.");
        }
    }

    const totalStudents = users.filter((user) => user.role === "student").length;
    const totalMentors = users.filter((user) => user.role === "mentor").length;
    const totalAdmins = users.filter((user) => user.role === "admin").length;

    return (
        <div className="user-management">
            <div className="um-heading">
                <div>
                    <p className="admin-eyebrow">ADMINISTRATION</p>
                    <h1>User Management</h1>
                    <p className="um-subtitle">
                        Manage student, mentor and administrator accounts.
                    </p>
                </div>

                <button
                    className="um-add-button"
                    type="button"
                    onClick={openAddModal}
                >
                    <Plus size={18} />
                    Add User
                </button>
            </div>

            <div className="um-summary-grid">
                <article className="um-summary-card">
                    <div className="um-summary-icon blue">
                        <Users size={21} />
                    </div>
                    <div>
                        <span>Total Users</span>
                        <h3>{users.length}</h3>
                    </div>
                </article>

                <article className="um-summary-card">
                    <div className="um-summary-icon orange">
                        <UserCheck size={21} />
                    </div>
                    <div>
                        <span>Students</span>
                        <h3>{totalStudents}</h3>
                    </div>
                </article>

                <article className="um-summary-card">
                    <div className="um-summary-icon purple">
                        <Users size={21} />
                    </div>
                    <div>
                        <span>Mentors</span>
                        <h3>{totalMentors}</h3>
                    </div>
                </article>

                <article className="um-summary-card">
                    <div className="um-summary-icon green">
                        <UserCheck size={21} />
                    </div>
                    <div>
                        <span>Admins</span>
                        <h3>{totalAdmins}</h3>
                    </div>
                </article>
            </div>

            <div className="um-table-panel">
                <div className="um-toolbar">
                    <div>
                        <h2>All Users</h2>
                        <p>View and manage registered platform users.</p>
                    </div>

                    <button
                        type="button"
                        className="um-refresh-button"
                        onClick={loadUsers}
                        disabled={loading}
                        aria-label="Refresh users"
                    >
                        <RefreshCw size={17} />
                    </button>
                </div>

                <div className="um-filters">
                    <label className="um-search">
                        <Search size={18} />
                        <input
                            type="search"
                            placeholder="Search by name, username or email..."
                            value={search}
                            onChange={(event) => setSearch(event.target.value)}
                        />
                    </label>

                    <select
                        value={roleFilter}
                        onChange={(event) => setRoleFilter(event.target.value)}
                        aria-label="Filter users by role"
                        className="um-role-filter"
                    >
                        <option value="all">All roles</option>
                        <option value="student">Students</option>
                        <option value="mentor">Mentors</option>
                        <option value="admin">Admins</option>
                    </select>
                </div>

                {error && !showModal && (
                    <div className="um-error">{error}</div>
                )}

                {loading ? (
                    <div className="um-empty">
                        <RefreshCw size={24} className="um-spinner" />
                        <p>Loading users...</p>
                    </div>
                ) : filteredUsers.length === 0 ? (
                    <div className="um-empty">
                        <Users size={30} />
                        <h3>No users found</h3>
                        <p>
                            {users.length === 0
                                ? "Registered users will appear here."
                                : "Try changing your search or role filter."}
                        </p>
                    </div>
                ) : (
                    <div className="um-table-wrapper">
                        <table className="um-table">
                            <thead>
                                <tr>
                                    <th>User</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Status</th>
                                    <th>Joined</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>

                            <tbody>
                                {filteredUsers.map((user) => (
                                    <tr key={user.id}>
                                        <td>
                                            <div className="um-user-cell">
                                                <div className="um-avatar">
                                                    {(user.first_name ||
                                                        user.username ||
                                                        "U")
                                                        .charAt(0)
                                                        .toUpperCase()}
                                                </div>

                                                <div>
                                                    <strong>
                                                        {`${user.first_name || ""} ${user.last_name || ""}`.trim() ||
                                                            user.username}
                                                    </strong>
                                                    <small>{user.username}</small>
                                                </div>
                                            </div>
                                        </td>

                                        <td>{user.email}</td>

                                        <td>
                                            <span className={`um-role ${user.role}`}>
                                                {user.role}
                                            </span>
                                        </td>

                                        <td>
                                            <span
                                                className={`um-status ${user.is_active ? "active" : "inactive"
                                                    }`}
                                            >
                                                {user.is_active ? "Active" : "Inactive"}
                                            </span>
                                        </td>

                                        <td>
                                            {user.date_joined
                                                ? new Date(user.date_joined).toLocaleDateString(
                                                    "en-IN",
                                                    {
                                                        day: "numeric",
                                                        month: "short",
                                                        year: "numeric",
                                                    }
                                                )
                                                : "—"}
                                        </td>

                                        <td>
                                            <div className="um-actions">
                                                <button
                                                    type="button"
                                                    title="Edit user"
                                                    onClick={() => openEditModal(user)}
                                                >
                                                    <Pencil size={16} />
                                                </button>

                                                <button
                                                    type="button"
                                                    title={
                                                        user.is_active
                                                            ? "Deactivate user"
                                                            : "Activate user"
                                                    }
                                                    onClick={() => handleStatusChange(user)}
                                                >
                                                    <UserCheck size={16} />
                                                </button>

                                                <button
                                                    type="button"
                                                    className="delete"
                                                    title="Delete user"
                                                    onClick={() => handleDelete(user)}
                                                >
                                                    <Trash2 size={16} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                <div className="um-table-footer">
                    Showing {filteredUsers.length} of {users.length} users
                </div>
            </div>

            {showModal && (
                <div className="um-modal-backdrop" onClick={closeModal}>
                    <div
                        className="um-modal"
                        onClick={(event) => event.stopPropagation()}
                    >
                        <div className="um-modal-heading">
                            <div>
                                <h2>{editingUser ? "Edit User" : "Add New User"}</h2>
                                <p>
                                    {editingUser
                                        ? "Update the user's account information."
                                        : "Create a new platform account."}
                                </p>
                            </div>

                            <button
                                type="button"
                                onClick={closeModal}
                                aria-label="Close modal"
                            >
                                <X size={20} />
                            </button>
                        </div>

                        {error && <div className="um-error">{error}</div>}

                        <form onSubmit={handleSubmit}>
                            <div className="um-form-grid">
                                <label>
                                    First name
                                    <input
                                        name="first_name"
                                        value={form.first_name}
                                        onChange={handleChange}
                                        placeholder="First name"
                                    />
                                </label>

                                <label>
                                    Last name
                                    <input
                                        name="last_name"
                                        value={form.last_name}
                                        onChange={handleChange}
                                        placeholder="Last name"
                                    />
                                </label>

                                <label className="full">
                                    Username
                                    <input
                                        name="username"
                                        value={form.username}
                                        onChange={handleChange}
                                        required
                                        placeholder="Username"
                                    />
                                </label>

                                <label className="full">
                                    Email address
                                    <input
                                        type="email"
                                        name="email"
                                        value={form.email}
                                        onChange={handleChange}
                                        required
                                        placeholder="Email address"
                                    />
                                </label>

                                {!editingUser && (
                                    <label className="full">
                                        Password
                                        <input
                                            type="password"
                                            name="password"
                                            value={form.password}
                                            onChange={handleChange}
                                            required
                                            minLength={8}
                                            placeholder="Minimum 8 characters"
                                        />
                                    </label>
                                )}

                                <label className="full">
                                    User role
                                    <select
                                        name="role"
                                        value={form.role}
                                        onChange={handleChange}
                                    >
                                        <option value="student">Student</option>
                                        <option value="mentor">Mentor</option>
                                        <option value="admin">Admin</option>
                                    </select>
                                </label>
                            </div>

                            <div className="um-modal-actions">
                                <button
                                    type="button"
                                    className="um-cancel-button"
                                    onClick={closeModal}
                                    disabled={saving}
                                >
                                    Cancel
                                </button>

                                <button
                                    type="submit"
                                    className="um-save-button"
                                    disabled={saving}
                                >
                                    {saving
                                        ? "Saving..."
                                        : editingUser
                                            ? "Save Changes"
                                            : "Create User"}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default UserManagement;
