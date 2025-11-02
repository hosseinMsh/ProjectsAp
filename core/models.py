from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Config(models.Model):
    register_deadline = models.DateTimeField(null=True, blank=True)
    choice_deadline = models.DateTimeField(null=True, blank=True)
    distribution_done = models.BooleanField(default=False)

    @classmethod
    def get_config(cls):
        cfg, _ = cls.objects.get_or_create(id=1)
        return cfg

    def is_register_open(self):
        return not self.register_deadline or timezone.now() < self.register_deadline

    def is_choice_open(self):
        return not self.choice_deadline or timezone.now() < self.choice_deadline

    def __str__(self):
        return "System Configuration"

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")], default="Medium")
    # one project can be assigned to at most one team
    assigned_team = models.OneToOneField("Team", null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_project")

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    representative = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="rep_teams")
    members = models.ManyToManyField("users.Student", related_name="teams", blank=True)

    project_choice_1 = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name="choice1_teams")
    project_choice_2 = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name="choice2_teams")
    project_choice_3 = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name="choice3_teams")

    final_project = models.OneToOneField(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name="final_team")

    STATUS_CHOICES = [("draft", "Draft"), ("submitted", "Submitted"), ("assigned", "Assigned")]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    def clean(self):
        if self.pk:
            # enforce size: two teams can have 4 members, others must have 3
            size = self.members.count() + 1  # include representative
            if size < 3:
                raise ValidationError(_("Team must have at least 3 members (including representative)."))
            if size > 4:
                raise ValidationError(_("Team cannot have more than 4 members."))

            # allow at most two teams of size 4
            if size == 4:
                four_count = Team.objects.exclude(pk=self.pk).annotate(
                    sz=models.Count("members")
                ).filter(sz=3).count()  # sz=3 + representative => 4
                if four_count >= 2:
                    raise ValidationError(_("Only two teams of size 4 are allowed."))

            # ensure final_project consistency with choices
            if self.final_project:
                if self.final_project not in [self.project_choice_1, self.project_choice_2, self.project_choice_3]:
                    raise ValidationError(_("Final project must be one of the three chosen projects."))

                # ensure project not assigned to other team
                if self.final_project.assigned_team and self.final_project.assigned_team_id != self.id:
                    raise ValidationError(_("This project is already assigned to another team."))

    def __str__(self):
        return f"{self.name}"
