
import { createContext, useContext, useState } from "react";
import { loginUser } from "../services/auth.service";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(() => {
        try {
            return JSON.parse(localStorage.getItem("user")) || null;
        } catch {
            return null;
        }
    });

    const [accessToken, setAccessToken] = useState(
        () => localStorage.getItem("access")
    );

    const [loading, setLoading] = useState(false);

    // Login
    const login = async (credentials) => {
        setLoading(true);

        try {
            const result = await loginUser(credentials);

            if (!result.user || !result.access) {
                throw new Error("Invalid login response from server.");
            }

            localStorage.setItem("user", JSON.stringify(result.user));
            localStorage.setItem("access", result.access);

            if (result.refresh) {
                localStorage.setItem("refresh", result.refresh);
            }

            setUser(result.user);
            setAccessToken(result.access);

            return result.user;
        } finally {
            setLoading(false);
        }
    };

    // Logout
    const logout = () => {
        localStorage.removeItem("user");
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");

        setUser(null);
        setAccessToken(null);
    };

    const isAuthenticated = Boolean(user && accessToken);

    const isAdmin =
        user?.role === "admin" ||
        user?.is_admin ||
        user?.is_staff ||
        user?.is_superuser;

    return (
        <AuthContext.Provider
            value={{
                user,
                accessToken,
                loading,
                isAuthenticated,
                isAdmin,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

// Custom authentication hook
export function useAuth() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error("useAuth must be used inside AuthProvider");
    }

    return context;
}
