
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import FeaturedCourses from "../components/FeaturedCourses";
import PlatformFeatures from "../components/PlatformFeatures";
import Footer from "../components/Footer";

function Home() {
    return (
        <>
            <Navbar />

            <main>
                <Hero />
                <FeaturedCourses />
                <PlatformFeatures />
                <Footer />
            </main>
        </>
    );
}

export default Home;
