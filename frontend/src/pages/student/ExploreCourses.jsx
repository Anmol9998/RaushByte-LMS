
import CourseCard from "../../components/common/CourseCard";
import "../../components/home/FeaturedCourses.css";
import { useEffect, useState } from "react";
import { BookOpen, Search } from "lucide-react";
import { getCourses } from "../../services/modules/courses.service";
import { useNavigate } from "react-router-dom";

import "./ExploreCourses.css";

function ExploreCourses() {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [search, setSearch] = useState("");
    const navigate = useNavigate();
    useEffect(() => {
        async function loadCourses() {
            try {
                const data = await getCourses();
                setCourses(Array.isArray(data) ? data : data.results || []);
            } catch (err) {
                console.error("Failed to load courses:", err);
                setError("Unable to load courses. Please try again.");
            } finally {
                setLoading(false);
            }
        }

        loadCourses();
    }, []);

    const filteredCourses = courses.filter((course) =>
        course.title?.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <section className="explore-courses">
            <div className="explore-header">
                <div>
                    <p>LEARN SOMETHING NEW</p>
                    <h2>Explore Courses</h2>
                    <span>Find courses and start building your skills.</span>
                </div>
            </div>

            <div className="course-search">
                <Search size={19} />
                <input
                    type="text"
                    placeholder="Search courses..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
            </div>

            {loading ? (
                <p>Loading courses...</p>
            ) : error ? (
                <p>{error}</p>
            ) : filteredCourses.length === 0 ? (
                <div className="explore-empty">
                    <BookOpen size={36} />
                    <h3>No courses found</h3>
                    <p>Try another search or check back later.</p>
                </div>
            ) : (

                <div className="explore-course-grid">
                    {filteredCourses.map((course) => (
                        <article className="course-card" key={course.id}>
                            <CourseCard
                                course={{
                                    ...course,
                                    color: course.color || "blue",
                                    icon: course.icon || "</>"
                                }}
                                actionLabel="View Course"
                                onAction={(selectedCourse) => {
                                    navigate(`/courses/${selectedCourse.id}`, {
                                        state: { from: "explore" },
                                    });
                                }}
                            />
                        </article>
                    ))}
                </div>

            )}
        </section>
    );
}

export default ExploreCourses;
