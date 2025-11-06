# projects/urls.py
from django.urls import path
from .views import team_create, team_manage, project_select, admin_assign, distribute_projects, export_csv, \
    teams_overview

urlpatterns = [
    path("team/create/", team_create, name="team_create"),
    path("team/<int:pk>/", team_manage, name="team_manage"),
    path("team/<int:pk>/select/", project_select, name="project_select"),
    path("admin/assign/", admin_assign, name="admin_assign"),
    path("teams/overview/", teams_overview, name="teams_overview"),

    path("distribute/", distribute_projects, name="distribute"),
    path("export/", export_csv, name="export_csv"),
]
