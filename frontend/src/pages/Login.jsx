
import { useState } from "react";
import { Link } from "react-router-dom";
import { Eye, EyeOff, BookOpen, ArrowRight } from "lucide-react";
import "./Login.css";
import { loginUser } from "../services/api";
import { useNavigate } from "react-router-dom";

function Login() {
    const [showPassword, setShowPassword] = useState(false);
    const [formData, setFormData] = useState({
        email: "",
        password: "",
        rememberMe: false,
    });
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleChange = (event) => {
        const { name, value, checked, type } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: type === "checkbox" ? checked : value,
        }));

        setMessage("");
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!formData.email.trim() || !formData.password) {
            setMessage("Please enter your email and password.");
            return;
        }

        try {
            const result = await loginUser({
                email: formData.email,
                password: formData.password,
            });

            // Save JWT tokens


            // Save the user information and JWT tokens
            localStorage.setItem("user", JSON.stringify(result));

            setMessage("Login successful!");

            const loggedInUser = result.user;

            if (
                loggedInUser?.is_admin ||
                loggedInUser?.is_staff ||
                loggedInUser?.is_superuser ||
                loggedInUser?.role === "admin"
            ) {
                navigate("/admin-dashboard", { replace: true });
            } else {
                navigate("/dashboard", { replace: true });
            }


        } catch (error) {
            if (error.detail) {
                setMessage(error.detail);
            } else {
                setMessage("Invalid email or password.");
            }
        }
    };
    return (
        <main className="login-page">
            <section className="login-visual">
                <Link to="/" className="login-brand">
                    <span className="login-brand-icon">
                        <BookOpen size={25} />
                    </span>
                    <span>
                        RaushByte <strong>Learn</strong>
                    </span>
                </Link>

                <div className="login-visual-content">
                    <span className="login-eyebrow">WELCOME BACK</span>

                    <h1>
                        Your next big
                        <br />
                        <span>step starts here.</span>
                    </h1>

                    <p>
                        Continue learning, build new skills, and move closer to your
                        goals. Your learning journey is waiting for you.
                    </p>

                    <div className="login-highlight">
                        <span className="login-highlight-dot" />
                        Learn something new today.
                    </div>
                </div>

                <div className="login-visual-footer">
                    Learn. Build. Grow.
                </div>
            </section>

            <section className="login-form-section">
                <div className="login-form-wrapper">
                    <Link to="/" className="login-mobile-brand">
                        RaushByte <strong>Learn</strong>
                    </Link>

                    <div className="login-heading">
                        <span className="login-small-label">YOUR LEARNING SPACE</span>
                        <h2>Welcome back!</h2>
                        <p>Enter your details to sign in to your account.</p>
                    </div>

                    <form className="login-form" onSubmit={handleSubmit}>
                        <div className="login-field">
                            <label htmlFor="login-email">Email address</label>
                            <input
                                id="login-email"
                                name="email"
                                type="email"
                                placeholder="you@example.com"
                                value={formData.email}
                                onChange={handleChange}
                                autoComplete="email"
                                required
                            />
                        </div>

                        <div className="login-field">
                            <div className="login-password-label">
                                <label htmlFor="login-password">Password</label>
                                <Link to="/forgot-password">Forgot password?</Link>
                            </div>

                            <div className="login-password-input">
                                <input
                                    id="login-password"
                                    name="password"
                                    type={showPassword ? "text" : "password"}
                                    placeholder="Enter your password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    autoComplete="current-password"
                                    required
                                />

                                <button
                                    type="button"
                                    className="login-eye-button"
                                    onClick={() => setShowPassword((previous) => !previous)}
                                    aria-label={showPassword ? "Hide password" : "Show password"}
                                >
                                    {showPassword ? <EyeOff size={19} /> : <Eye size={19} />}
                                </button>
                            </div>
                        </div>

                        <label className="login-remember">
                            <input
                                type="checkbox"
                                name="rememberMe"
                                checked={formData.rememberMe}
                                onChange={handleChange}
                            />
                            <span>Remember me</span>
                        </label>

                        {message && (
                            <p className="login-message" role="status">
                                {message}
                            </p>
                        )}

                        <button className="login-submit" type="submit">
                            Sign in <ArrowRight size={19} />
                        </button>
                    </form>

                    <div className="login-divider">
                        <span>NEW TO RAUSHBYTE?</span>
                    </div>

                    <p className="login-register">
                        Don't have an account? <Link to="/register">Create one</Link>
                    </p>

                    <p className="login-terms">
                        By continuing, you agree to our <a href="#terms">Terms</a> and{" "}
                        <a href="#privacy">Privacy Policy</a>.
                    </p>
                </div>
            </section>
        </main>
    );
}

export default Login;
