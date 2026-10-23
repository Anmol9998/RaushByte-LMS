
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import FeaturedCourses from "../components/FeaturedCourses";
import PlatformFeatures from "../components/PlatformFeatures";

function Home() {
    return (
        <>
            <Navbar />

            <main>
                <Hero />
                <FeaturedCourses />
                <PlatformFeatures />
            </main>
        </>
    );
}

export default Home;
