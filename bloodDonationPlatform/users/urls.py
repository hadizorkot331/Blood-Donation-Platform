from django.urls import path
from . import views


app_name = "users"


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("complete-profile/", views.complete_profile, name="complete-profile"),
    path("edit-profile/", views.edit_profile, name="edit-profile"),
]
