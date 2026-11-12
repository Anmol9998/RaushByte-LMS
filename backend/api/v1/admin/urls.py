from django.urls import re_path
from .views import (
	AdminDashboardSummaryView,
	AdminLoginView,
	UserDetailView,
	UserListCreateView,
)

urlpatterns = [
	re_path(r"login/$", AdminLoginView.as_view(), name="admin-login"),
	re_path(r"dashboard/$", AdminDashboardSummaryView.as_view(), name="admin-dashboard"),
	re_path(r"users/$", UserListCreateView.as_view(), name="user-list"),
	re_path(r"users/(?P<pk>[^/.]+)/$", UserDetailView.as_view(), name="user-detail"),
]