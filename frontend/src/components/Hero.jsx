
import { motion } from "motion/react";
import "./Hero.css";

function Hero() {
    return (
        <section className="hero-section" id="home">
            <motion.div
                className="hero-content"
                initial={{ opacity: 0, y: 25 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, ease: "easeOut" }}
            >
                <span className="hero-tag">
                    LEARN. BUILD. GROW.
                </span>

                <h1>
                    Build your skills.
                    <br />
                    Shape your <span>future.</span>
                </h1>

                <p className="hero-description">
                    Learn new technologies, work on practical assignments,
                    and grow with guidance from mentors. Your next step
                    starts here.
                </p>

                <div className="hero-buttons">
                    <a href="#courses" className="hero-primary-btn">
                        Explore Courses
                        <span aria-hidden="true">&rarr;</span>
                    </a>

                    <a href="#about" className="hero-secondary-btn">
                        Discover RaushByte
                    </a>
                </div>

                <div className="hero-highlights">
                    <div className="hero-highlight">
                        <span className="highlight-dot blue-dot"></span>
                        Practical Learning
                    </div>

                    <div className="hero-highlight">
                        <span className="highlight-dot green-dot"></span>
                        Mentor Guidance
                    </div>

                    <div className="hero-highlight">
                        <span className="highlight-dot orange-dot"></span>
                        Track Your Progress
                    </div>
                </div>
            </motion.div>

            <motion.div
                className="hero-visual"
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{
                    duration: 0.8,
                    delay: 0.15,
                    ease: "easeOut"
                }}
            >
                <div className="visual-heading">
                    <div>
                        <span className="visual-eyebrow">
                            YOUR LEARNING SPACE
                        </span>
                        <h2>Keep moving forward.</h2>
                    </div>

                    <span className="visual-icon" aria-hidden="true">
                        &#10003;
                    </span>
                </div>

                <div className="learning-card">
                    <div className="learning-card-icon react-icon">
                        R
                    </div>

                    <div className="learning-card-info">
                        <h3>Web Development</h3>
                        <p>Learn by building real projects</p>
                    </div>

                    <span className="card-arrow" aria-hidden="true">
                        &rarr;
                    </span>
                </div>

                <div className="learning-card">
                    <div className="learning-card-icon python-icon">
                        P
                    </div>

                    <div className="learning-card-info">
                        <h3>Python Programming</h3>
                        <p>Strengthen your coding skills</p>
                    </div>

                    <span className="card-arrow" aria-hidden="true">
                        &rarr;
                    </span>
                </div>

                <div className="progress-card">
                    <div className="progress-card-top">
                        <div>
                            <span className="progress-label">
                                YOUR NEXT MILESTONE
                            </span>
                            <h3>Keep learning, keep growing</h3>
                        </div>

                        <span className="progress-check" aria-hidden="true">
                            &#10003;
                        </span>
                    </div>

                    <div className="progress-track">
                        <div className="progress-fill"></div>
                    </div>

                    <p>
                        Courses, assignments, and progress — all in one place.
                    </p>
                </div>

                <div className="hero-decoration decoration-one"></div>
                <div className="hero-decoration decoration-two"></div>
            </motion.div>
        </section>
    );
}

export default Hero;
