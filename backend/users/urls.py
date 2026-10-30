from django.urls import path
from .views import ( RegisterView, LoginView, 
AdminDashboardSummaryView, UserListCreateView,
    UserDetailView,
)



urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("admin/dashboard/", AdminDashboardSummaryView.as_view(), name="admin-dashboard"),
    path("users/", UserListCreateView.as_view(), name="user-list"),
    path("users/<str:pk>/", UserDetailView.as_view(), name="user-detail"),
    ]