
import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, adminOnly = false }) {
    const token = localStorage.getItem("access");
    const storedUser = localStorage.getItem("user");

    if (!token || !storedUser) {
        return <Navigate to="/login" replace />;
    }

    let user;

    try {
        const parsedUser = JSON.parse(storedUser);
        user = parsedUser.user || parsedUser;
    } catch {
        return <Navigate to="/login" replace />;
    }

    if (adminOnly && user.role !== "admin" && !user.is_admin) {
        return <Navigate to="/dashboard" replace />;
    }

    return children;
}

export default ProtectedRoute;
