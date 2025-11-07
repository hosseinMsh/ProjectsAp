from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student

@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ("username", "student_id", "first_name", "last_name", "github_username", "is_representative")
    search_fields = ("username", "student_id", "first_name", "last_name", "github_username")

    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {
            "fields": (
                "student_id",
                "github_email",
                "github_username",
                "telegram_link",
                "is_representative",
                "must_change_password",
            )
        }),
    )
