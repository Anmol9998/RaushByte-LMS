
import "./Footer.css";

function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="site-footer">
            <div className="footer-container">
                <div className="footer-main">
                    <div className="footer-brand">
                        <a href="#home" className="footer-logo">
                            <span className="footer-logo-icon">R</span>
                            <span>RaushByte Learn</span>
                        </a>

                        <p className="footer-description">
                            Learn new technologies, build practical skills, and
                            take the next step in your learning journey.
                        </p>
                    </div>

                    <div className="footer-links-group">
                        <h3>Explore</h3>
                        <a href="#home">Home</a>
                        <a href="#courses">Courses</a>
                        <a href="#features">Features</a>
                    </div>

                    <div className="footer-links-group">
                        <h3>Learning</h3>
                        <a href="#courses">Explore Courses</a>
                        <a href="#features">How It Works</a>
                    </div>

                    <div className="footer-links-group">
                        <h3>Get Started</h3>
                        <a href="#login">Log in</a>
                        <a href="#courses">Start Learning</a>
                    </div>
                </div>

                <div className="footer-bottom">
                    <p>
                        &copy; {currentYear} RaushByte Learn. All rights reserved.
                    </p>

                    <a href="#home" className="footer-back-to-top">
                        Back to top <span aria-hidden="true">&uarr;</span>
                    </a>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
