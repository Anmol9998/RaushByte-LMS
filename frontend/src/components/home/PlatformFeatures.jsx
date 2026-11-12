
import "./PlatformFeatures.css";

const features = [
    {
        id: 1,
        icon: "01",
        title: "Structured Learning",
        description:
            "Access organized courses, learning modules, lessons, and resources in one place.",
        color: "feature-blue",
    },
    {
        id: 2,
        icon: "02",
        title: "Internship Batches",
        description:
            "Follow your assigned batch, stay updated with schedules, and keep track of learning activities.",
        color: "feature-purple",
    },
    {
        id: 3,
        icon: "03",
        title: "Assignments & Feedback",
        description:
            "Submit projects, share GitHub links, and receive feedback and grades from your mentor.",
        color: "feature-orange",
    },
    {
        id: 4,
        icon: "04",
        title: "Progress Tracking",
        description:
            "Monitor lesson completion, assignment status, and your progress toward course milestones.",
        color: "feature-green",
    },
    {
        id: 5,
        icon: "05",
        title: "Course Certificates",
        description:
            "Access certificates when you meet the platform's required completion criteria.",
        color: "feature-pink",
    },
    {
        id: 6,
        icon: "06",
        title: "Updates & Notifications",
        description:
            "Stay informed about deadlines, mentor feedback, and important announcements.",
        color: "feature-teal",
    },
];

function PlatformFeatures() {
    return (
        <section className="features-section" id="features">
            <div className="features-container">
                <div className="features-heading">
                    <span className="section-label">
                        EVERYTHING IN ONE PLACE
                    </span>

                    <h2>
                        Everything you need to <span>keep growing.</span>
                    </h2>

                    <p>
                        From your first lesson to your final project,
                        RaushByte Learn brings your learning journey together.
                    </p>
                </div>

                <div className="features-grid">
                    {features.map((feature) => (
                        <article className="feature-card" key={feature.id}>
                            <div
                                className={`feature-icon ${feature.color}`}
                                aria-hidden="true"
                            >
                                {feature.icon}
                            </div>

                            <h3>{feature.title}</h3>

                            <p>{feature.description}</p>

                            <span className="feature-arrow" aria-hidden="true">
                                &#8599;
                            </span>
                        </article>
                    ))}
                </div>
            </div>
        </section>
    );
}

export default PlatformFeatures;
