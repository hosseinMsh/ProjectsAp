from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):
    student_id = models.CharField(max_length=10, unique=True)
    github_email = models.EmailField(blank=True, null=True)
    github_username = models.CharField(max_length=100, blank=True, null=True)
    telegram_link = models.CharField(max_length=100, blank=True, null=True)
    is_representative = models.BooleanField(default=True)
    must_change_password = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name()} - {self.student_id}"
