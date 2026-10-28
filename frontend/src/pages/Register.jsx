
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../services/api";
import "./Register.css";

function Register() {
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
    });

    const [message, setMessage] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleChange = (event) => {
        const { name, value } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: value,
        }));

        setMessage("");
    };

    const handleSubmit = async (event) => {
    event.preventDefault();

    if (formData.password.length < 8) {
        setMessage("Password must contain at least 8 characters.");
        return;
    }

    if (formData.password !== formData.confirmPassword) {
        setMessage("Passwords do not match.");
        return;
    }

    try {
        const result = await registerUser(formData);

        setMessage(result.message || "Registration successful!");

        // Redirect to Login page after 2 seconds
        setTimeout(() => {
            navigate("/login");
        }, 2000);

    } catch (error) {

        if (error.email) {
            setMessage(error.email[0]);
        } else if (error.username) {
            setMessage(error.username[0]);
        } else if (error.confirmPassword) {
            setMessage(error.confirmPassword[0]);
        } else {
            setMessage("Registration failed.");
        }
    }
};

    return (
        <main className="register-page">
            <div className="register-decoration register-decoration-one" />
            <div className="register-decoration register-decoration-two" />

            <a href="/" className="register-brand">
                <span className="brand-mark">R</span>
                <span>
                    RaushByte<span className="brand-highlight"> Learn</span>
                </span>
            </a>

            <section className="register-card">
                <div className="register-heading">
                    <span className="register-eyebrow">START YOUR JOURNEY</span>
                    <h1>Create your account<span>.</span></h1>
                    <p>
                        Learn new skills, explore courses, and take the next step
                        in your learning journey.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="register-form">
                    <div className="register-name-row">
                        <div className="register-field">
                            <label htmlFor="first_name">First name</label>
                            <input
                                id="first_name"
                                name="first_name"
                                type="text"
                                placeholder="First name"
                                value={formData.first_name}
                                onChange={handleChange}
                                autoComplete="given-name"
                                required
                            />
                        </div>

                        <div className="register-field">
                            <label htmlFor="last_name">Last name</label>
                            <input
                                id="last_name"
                                name="last_name"
                                type="text"
                                placeholder="Last name"
                                value={formData.last_name}
                                onChange={handleChange}
                                autoComplete="family-name"
                                required
                            />
                        </div>
                    </div>

                    <div className="register-field">
                        <label htmlFor="username">Username</label>
                        <input
                            id="username"
                            name="username"
                            type="text"
                            placeholder="Choose a username"
                            value={formData.username}
                            onChange={handleChange}
                            autoComplete="username"
                            required
                        />
                    </div>

                    <div className="register-field">
                        <label htmlFor="email">Email address</label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            placeholder="you@example.com"
                            value={formData.email}
                            onChange={handleChange}
                            autoComplete="email"
                            required
                        />
                    </div>

                    <div className="register-field">
                        <label htmlFor="password">Password</label>

                        <div className="register-password-wrap">
                            <input
                                id="password"
                                name="password"
                                type={showPassword ? "text" : "password"}
                                placeholder="At least 8 characters"
                                value={formData.password}
                                onChange={handleChange}
                                autoComplete="new-password"
                                minLength={8}
                                required
                            />

                            <button
                                type="button"
                                className="password-toggle"
                                onClick={() => setShowPassword((previous) => !previous)}
                                aria-label={showPassword ? "Hide password" : "Show password"}
                            >
                                {showPassword ? "Hide" : "Show"}
                            </button>
                        </div>
                    </div>

                    <div className="register-field">
                        <label htmlFor="confirmPassword">Confirm password</label>
                        <input
                            id="confirmPassword"
                            name="confirmPassword"
                            type={showPassword ? "text" : "password"}
                            placeholder="Enter your password again"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            autoComplete="new-password"
                            required
                        />
                    </div>

                    {message && (
                        <p
                            className={
                                message.toLowerCase().includes("successful")

                                    ? "register-message success"
                                    : "register-message error"
                            }
                            role="status"
                        >
                            {message}
                        </p>
                    )}

                    <button type="submit" className="register-submit">
                        Create Account <span aria-hidden="true">→</span>
                    </button>

                    <p className="register-terms">
                        By creating an account, you agree to use RaushByte Learn
                        responsibly.
                    </p>
                </form>

                <div className="register-login">
                    Already have an account? <a href="/login">Log in</a>
                </div>
            </section>

            <p className="register-footer">
                Learn. Build. Grow. <span>© RaushByte Learn</span>
            </p>
        </main>
    );
}

export default Register;
