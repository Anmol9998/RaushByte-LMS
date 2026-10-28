
import { useState } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
    const [menuOpen, setMenuOpen] = useState(false);

    const closeMenu = () => {
        setMenuOpen(false);
    };

    return (
        <header className="navbar">
            <Link to="/" className="navbar-brand" onClick={closeMenu}>
                <span className="brand-logo">R</span>
                <span className="brand-name">RaushByte Learn</span>
            </Link>

            <button
                className={`hamburger ${menuOpen ? "active" : ""}`}
                type="button"
                aria-label={
                    menuOpen
                        ? "Close navigation menu"
                        : "Open navigation menu"
                }
                aria-expanded={menuOpen}
                aria-controls="navbar-links"
                onClick={() => setMenuOpen((open) => !open)}
            >
                <span></span>
                <span></span>
                <span></span>
            </button>

            <nav
                id="navbar-links"
                className={`navbar-links ${menuOpen ? "open" : ""}`}
            >
                <Link to="/" onClick={closeMenu}>Home</Link>
                <a href="#courses" onClick={closeMenu}>Courses</a>
                <a href="#features" onClick={closeMenu}>Features</a>
                <a href="#about" onClick={closeMenu}>About</a>

                <div className="mobile-actions">
                    <Link
                        to="/login"
                        className="mobile-login"
                        onClick={closeMenu}
                    >
                        Log in
                    </Link>

                    <a
                        href="#courses"
                        className="mobile-explore"
                        onClick={closeMenu}
                    >
                        Explore Courses
                    </a>
                </div>
            </nav>

            <div className="navbar-actions">
                <Link to="/login" className="navbar-login">
                    Log in
                </Link>

                <a href="#courses" className="navbar-explore">
                    Explore Courses
                </a>
            </div>
        </header>
    );
}

export default Navbar;
