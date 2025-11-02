# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
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

class StudentCSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="فایل CSV دانشجویان",
        help_text="فایل باید شامل ستون‌های student_id و email باشد."
    )

class PersianPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "رمز عبور فعلی"
        self.fields["new_password1"].label = "رمز عبور جدید"
        self.fields["new_password2"].label = "تأیید رمز عبور جدید"

        self.fields["old_password"].help_text = ""
        self.fields["new_password1"].help_text = "رمز جدید باید حداقل ۸ کاراکتر و ترکیبی از عدد و حرف باشد."
        self.fields["new_password2"].help_text = "رمز جدید را دوباره برای تأیید وارد کنید."

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand focus:border-brand",
                "autocomplete": "off",
                "dir": "ltr"
            })