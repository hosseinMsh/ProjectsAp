import csv, secrets
from django.contrib.auth import get_user_model

def create_students_from_csv(file):
    User = get_user_model()
    created_users = []
    decoded = file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    for row in reader:
        sid = row["student_id"].strip()
        email = row.get("email","").strip()
        first_name = row.get("first_name","").strip()
        last_name = row.get("last_name","").strip()
        password = secrets.token_urlsafe(8)
        user, created = User.objects.get_or_create(
            student_id=sid,
            defaults={
                "username": sid,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "is_representative": True,
                "must_change_password": True,
            }

        )
        if created:
            user.set_password(password)
            user.save()
            created_users.append((sid, email, password))
    return created_users
