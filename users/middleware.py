import time
from django.shortcuts import redirect
from django.urls import reverse
from django.core.cache import cache
from django.contrib import messages

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

class LoginRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse("users:login") and request.method == "POST":
            ip = request.META.get("REMOTE_ADDR")
            key = f"login_attempts_{ip}"
            attempts = cache.get(key, 0) + 1
            cache.set(key, attempts, timeout=60)

            if attempts > 5:
                messages.error(request, "⚠️ تعداد تلاش‌های ورود زیاد بوده است. لطفاً یک دقیقه دیگر تلاش کنید.")
                time.sleep(2)
                return redirect("users:login")

        return self.get_response(request)