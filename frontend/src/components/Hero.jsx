
import { motion } from "motion/react";
import "./Hero.css";

function Hero() {
    return (
        <section className="hero-section" id="home">
            <div className="hero-container">
                {/* Left side: Hero content */}
                <motion.div
                    className="hero-content"
                    initial={{ opacity: 0, y: 25 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.7, ease: "easeOut" }}
                >
                    <span className="hero-tag">LEARN. BUILD. GROW.</span>

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
                            <span className="highlight-dot orange-dot"></span>
                            Practical Learning
                        </div>

                        <div className="hero-highlight">
                            <span className="highlight-dot orange-dot"></span>
                            Mentor Guidance
                        </div>

                        <div className="hero-highlight">
                            <span className="highlight-dot orange-dot"></span>
                            Track Your Progress
                        </div>
                    </div>
                </motion.div>

                {/* Right side: Programming image */}
                <motion.div
                    className="hero-image-wrapper"
                    initial={{ opacity: 0, x: 30 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                >
                    <div className="hero-image-glow"></div>

                    <img
                        src="/images/hero-tech.png"
                        alt="Student learning programming with coding illustrations"
                        className="hero-image"
                    />
                </motion.div>
            </div>
        </section>
    );
}

export default Hero;
