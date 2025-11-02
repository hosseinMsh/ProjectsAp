from django.contrib import admin
from core.models import Project, Team

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "assigned_team")
    search_fields = ("title",)
    list_filter = ("level",)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "representative", "status", "final_project")
    search_fields = ("name", "representative__username")
    list_filter = ("status",)
