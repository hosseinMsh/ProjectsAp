# projects/forms.py
from django import forms
from .models import Team, Project

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name"]
        labels = {"name": "نام تیم"}
        help_texts = {
            "name": "نام تیم باید یکتا باشد و فقط شامل حروف انگلیسی، عدد یا خط تیره باشد."
        }
        error_messages = {
            "name": {
                "required": "لطفاً یک نام برای تیم خود وارد کنید.",
                "unique": "تیمی با این نام از قبل وجود دارد.",
            },
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError("نام تیم باید حداقل ۳ کاراکتر باشد.")
        return name


class TeamMembersForm(forms.Form):
    member_student_ids = forms.CharField(
        label="شماره‌های دانشجویی اعضا",
        widget=forms.Textarea(attrs={
            "placeholder": "هر شماره دانشجویی را در یک خط بنویسید (بدون نماینده)...",
            "rows": 6,
            "dir": "ltr"
        }),
        help_text="شماره دانشجویی هر عضو را جداگانه در خط جدید وارد کنید.",
        required=False,
    )

class ProjectChoiceForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["project_choice_1", "project_choice_2", "project_choice_3"]
        labels = {
            "project_choice_1": "اولویت اول",
            "project_choice_2": "اولویت دوم",
            "project_choice_3": "اولویت سوم",
        }
        error_messages = {
            "project_choice_1": {"required": "لطفاً پروژه‌ی اول را انتخاب کنید."},
            "project_choice_2": {"required": "لطفاً پروژه‌ی دوم را انتخاب کنید."},
            "project_choice_3": {"required": "لطفاً پروژه‌ی سوم را انتخاب کنید."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = Project.objects.filter(assigned_team__isnull=True)
        for i in range(1, 4):
            self.fields[f"project_choice_{i}"].queryset = qs
            self.fields[f"project_choice_{i}"].empty_label = f"— انتخاب پروژه‌ی {i} —"

    def clean(self):
        cleaned = super().clean()
        p1, p2, p3 = cleaned.get("project_choice_1"), cleaned.get("project_choice_2"), cleaned.get("project_choice_3")
        chosen = [p for p in [p1, p2, p3] if p]
        if len(chosen) != 3:
            raise forms.ValidationError("لطفاً دقیقاً سه پروژه متفاوت انتخاب کنید.")
        if len(set(chosen)) != len(chosen):
            raise forms.ValidationError("پروژه‌ها باید متفاوت باشند.")
        return cleaned
