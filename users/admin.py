# users/admin.py
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("username", "student_id", "first_name", "last_name", "github_username", "is_representative")
    search_fields = ("username", "student_id", "first_name", "last_name", "github_username")
