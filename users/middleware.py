from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        if user and user.is_authenticated and getattr(user, "must_change_password", False):
            path = request.path
            allowed_paths = [
                reverse("users:force_password_change"),
                reverse("users:logout"),
            ]
            if path not in allowed_paths and not path.startswith("/admin/"):
                return redirect("users:force_password_change")

        return self.get_response(request)
