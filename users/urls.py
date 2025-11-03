# users/urls.py
from django.urls import path
from users.views import register, login_view, upload_students, force_password_change, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page='users:login'), name="logout"),
    path("upload-students/", upload_students, name="upload_students"),
    path("change-password/", force_password_change, name="force_password_change"),
    path("profile/", profile_view, name="profile"),

]
