# projects/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from users.models import Student
from .models import Team, Project, Config
from .forms import TeamCreateForm, TeamMembersForm, ProjectChoiceForm
import csv

@staff_member_required
def distribute_projects(request):
    cfg = Config.get_config()
    teams = Team.objects.filter(status="submitted").order_by("name")
    assigned = 0
    skipped = []

    if request.method == "POST":
        # auto assign mode
        for team in teams:
            for choice in [team.project_choice_1, team.project_choice_2, team.project_choice_3]:
                if choice and not choice.assigned_team:
                    team.final_project = choice
                    team.status = "assigned"
                    team.save()
                    choice.assigned_team = team
                    choice.save()
                    assigned += 1
                    break
            else:
                skipped.append(team.name)
        cfg.distribution_done = True
        cfg.save()
        messages.success(request, f"{assigned} تیم تخصیص داده شدند؛ {len(skipped)} تیم بدون پروژه ماندند.")
        if skipped:
            messages.warning(request, "تیم‌های بدون پروژه: " + ", ".join(skipped))
        return redirect("projects:distribute")

    return render(request, "projects/distribute.html", {"teams": teams, "cfg": cfg, "assigned": assigned, "skipped": skipped})

@staff_member_required
def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="teams_projects.csv"'
    writer = csv.writer(response)
    writer.writerow(["Team Name", "Representative", "Members", "Final Project"])
    for t in Team.objects.select_related("representative", "final_project"):
        members = ", ".join([m.get_full_name() for m in t.members.all()])
        writer.writerow([t.name, t.representative.get_full_name(), members, t.final_project.title if t.final_project else ""])
    return response

def _is_rep(user):
    """Check if the user is a representative"""
    return getattr(user, "is_representative", False)


@login_required
def team_create(request):
    user = request.user

    
    if not _is_rep(user):
        messages.error(request, "❌ فقط نماینده‌ها می‌توانند تیم ایجاد کنند.")
        return redirect("dashboard")

    if hasattr(user, "rep_teams"):
        messages.warning(request, "⚠️ شما قبلاً یک تیم ساخته‌اید و نمی‌توانید تیم جدیدی ایجاد کنید.")
        return redirect("dashboard")

    if request.method == "POST":
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.representative = user
            team.save()


            team.members.add(user)
            user.is_representative = True
            user.save(update_fields=["is_representative"])

            messages.success(request, f"✅ تیم «{team.name}» با موفقیت ایجاد شد.")
            return redirect("projects:team_manage", pk=team.pk)
        else:
            messages.error(request, "❌ اطلاعات وارد شده معتبر نیست. لطفاً دوباره بررسی کنید.")
    else:
        form = TeamCreateForm()

    return render(request, "projects/team_create.html", {"form": form})

@login_required
def team_manage(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if team.representative != request.user:
        messages.error(request, "Only the representative can manage this team.")
        return redirect("dashboard")

    if request.method == "POST":
        form = TeamMembersForm(request.POST)
        if form.is_valid():
            ids = [s.strip() for s in form.cleaned_data["member_student_ids"].splitlines() if s.strip()]
            with transaction.atomic():
                # clear all except representative (kept)
                team.members.set([request.user])
                for sid in ids:
                    try:
                        stu = Student.objects.get(student_id=sid)
                        if stu == request.user:
                            continue
                        team.members.add(stu)
                    except Student.DoesNotExist:
                        messages.warning(request, f"Student ID not found: {sid}")
                try:
                    team.full_clean()
                    team.save()
                    messages.success(request, "Members updated.")
                except Exception as e:
                    transaction.set_rollback(True)
                    messages.error(request, str(e))
            return redirect("projects:team_manage", pk=team.pk)
    else:
        form = TeamMembersForm()

    size = team.members.count()  # includes representative now
    return render(request, "projects/team_manage.html", {"team": team, "form": form, "size": size})

@login_required
def project_select(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if team.representative != request.user:
        messages.error(request, "Only the representative can select projects.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ProjectChoiceForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            team.status = "submitted"
            team.save()
            messages.success(request, "Project choices submitted.")
            return redirect("dashboard")
    else:
        form = ProjectChoiceForm(instance=team)

    return render(request, "projects/project_select.html", {"team": team, "form": form})

@staff_member_required
def admin_assign(request):
    teams = Team.objects.select_related("final_project").all().order_by("name")
    projects = Project.objects.all().order_by("title")

    if request.method == "POST":
        team_id = request.POST.get("team_id")
        project_id = request.POST.get("project_id")
        team = get_object_or_404(Team, pk=team_id)
        project = get_object_or_404(Project, pk=project_id)

        if project not in [team.project_choice_1, team.project_choice_2, team.project_choice_3]:
            messages.error(request, "Selected project is not among team's choices.")
            return redirect("projects:admin_assign")

        if project.assigned_team and project.assigned_team_id != team.id:
            messages.error(request, "Project already assigned to another team.")
            return redirect("projects:admin_assign")

        with transaction.atomic():
            team.final_project = project
            team.status = "assigned"
            team.full_clean()
            team.save()
            project.assigned_team = team
            project.save()
        messages.success(request, f"Assigned '{project.title}' to '{team.name}'.")
        return redirect("projects:admin_assign")

    return render(request, "projects/admin_assign.html", {"teams": teams, "projects": projects})
