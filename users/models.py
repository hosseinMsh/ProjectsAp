from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):
    # username remains; we will store student specific fields
    student_id = models.CharField(max_length=15, unique=True)
    github_username = models.CharField(max_length=50)
    github_email = models.EmailField()
    telegram_link = models.URLField(blank=True)
    is_representative = models.BooleanField(default=False)

    # enforce email as required login-facing field? keep default auth
    def __str__(self):
        return f"{self.get_full_name()} - {self.student_id}"
