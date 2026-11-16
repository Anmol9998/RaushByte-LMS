from django.urls import re_path
from .views import (
    MentorAssignedCoursesView,
    MentorCourseDetailView,
    MentorCourseModulesView,
    MentorCourseLessonsView,
    MentorCourseStudentsView,
    MentorCourseStatisticsView,
    MentorCourseCurriculumView,
)

urlpatterns = [
    re_path(r"^$", MentorAssignedCoursesView.as_view(), name="mentor-assigned-courses"),
    re_path(
        r"^(?P<course_id>[^/.]+)/?$",
        MentorCourseDetailView.as_view(),
        name="mentor-course-detail",
    ),
    re_path(
        r"^(?P<course_id>[^/.]+)/modules/?$",
        MentorCourseModulesView.as_view(),
        name="mentor-course-modules",
    ),
    re_path(
        r"^(?P<course_id>[^/.]+)/lessons/?$",
        MentorCourseLessonsView.as_view(),
        name="mentor-course-lessons",
    ),
    re_path(
        r"^(?P<course_id>[^/.]+)/students/?$",
        MentorCourseStudentsView.as_view(),
        name="mentor-course-students",
    ),
    re_path(
        r"^(?P<course_id>[^/.]+)/statistics/?$",
        MentorCourseStatisticsView.as_view(),
        name="mentor-course-statistics",
    ),
    re_path(
        r"^(?P<course_id>[^/.]+)/curriculum/?$",
        MentorCourseCurriculumView.as_view(),
        name="mentor-course-curriculum",
    ),
]