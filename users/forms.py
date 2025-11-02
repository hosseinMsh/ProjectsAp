# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student

class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = Student
        fields = [
            "username",
            "first_name",
            "last_name",
            "student_id",
            "email",
            "github_email",
            "github_username",
            "telegram_link",
            "password1",
            "password2",
        ]
        labels = {
            "username": "نام کاربری",
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "student_id": "شماره دانشجویی",
            "email": "ایمیل دانشگاهی",
            "github_email": "ایمیل متصل به GitHub",
            "github_username": "نام کاربری GitHub",
            "telegram_link": "آدرس تلگرام",
            "password1": "رمز عبور",
            "password2": "تأیید رمز عبور",
        }
        help_texts = {
            "username": "فقط حروف انگلیسی، اعداد و نشانه‌های @ . + - _ مجاز هستند.",
            "password1": "رمز عبور باید حداقل ۸ کاراکتر و ترکیبی از حروف و اعداد باشد.",
            "password2": "رمز عبور را برای تأیید دوباره وارد کنید.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = self.Meta.help_texts.get(fieldname, "")
            self.fields[fieldname].label = self.Meta.labels.get(fieldname, "")


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(label="نام کاربری یا شماره دانشجویی")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)