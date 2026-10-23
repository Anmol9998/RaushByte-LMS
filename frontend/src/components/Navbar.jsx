
import { useState } from "react";
import "./Navbar.css";

function Navbar() {
    const [menuOpen, setMenuOpen] = useState(false);

    const closeMenu = () => {
        setMenuOpen(false);
    };

    return (
        <header className="navbar">
            <a href="#home" className="navbar-brand" onClick={closeMenu}>
                <span className="brand-logo">R</span>
                <span className="brand-name">RaushByte Learn</span>
            </a>

            <button
                className={`hamburger ${menuOpen ? "active" : ""}`}
                type="button"
                aria-label={menuOpen ? "Close navigation menu" : "Open navigation menu"}
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
                <a href="#home" onClick={closeMenu}>Home</a>
                <a href="#courses" onClick={closeMenu}>Courses</a>
                <a href="#features" onClick={closeMenu}>Features</a>
                <a href="#about" onClick={closeMenu}>About</a>

                <div className="mobile-actions">
                    <a href="#login" className="mobile-login" onClick={closeMenu}>
                        Log in
                    </a>
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
                <a href="#login" className="navbar-login">
                    Log in
                </a>
                <a href="#courses" className="navbar-explore">
                    Explore Courses
                </a>
            </div>
        </header>
    );
}

export default Navbar;
