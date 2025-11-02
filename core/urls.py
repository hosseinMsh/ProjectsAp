# projects/urls.py
from django.urls import path
from .views import team_create, team_manage, project_select, admin_assign, distribute_projects, export_csv

urlpatterns = [
    path("team/create/", team_create, name="team_create"),
    path("team/<int:pk>/", team_manage, name="team_manage"),
    path("team/<int:pk>/select/", project_select, name="project_select"),
    path("admin/assign/", admin_assign, name="admin_assign"),
    path("distribute/", distribute_projects, name="distribute"),
    path("export/", export_csv, name="export_csv"),
]
