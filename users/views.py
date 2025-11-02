# users/views.py
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import StudentRegisterForm, StudentLoginForm
from django.contrib.auth import authenticate

def register(request):
    if request.method == "POST":
        print("Aaa")
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
        print(form.errors)
        return render(request, "users/register.html", {"form": form})
    else:
        form = StudentRegisterForm()
    print("Sdsad")
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    form = StudentLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("dashboard")
    return render(request, "users/login.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@staff_member_required
def upload_students(request):
    result = None
    if request.method == "POST":
        form = StudentCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["csv_file"]
            created_users = create_students_from_csv(file)

            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="created_students.csv"'
            writer = csv.writer(response)
            writer.writerow(["student_id", "email", "password"])
            for sid, email, pwd in created_users:
                writer.writerow([sid, email, pwd])
            return response
    else:
        form = StudentCSVUploadForm()
    return render(request, "users/upload_students.html", {"form": form})


@login_required
def force_password_change(request):
    """Require students to change password after first login"""
    user = request.user
    form = PersianPasswordChangeForm(user, request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            user.must_change_password = False
            user.save(update_fields=["must_change_password"])
            update_session_auth_hash(request, user)
            messages.success(request, "✅ رمز عبور شما با موفقیت تغییر کرد.")
            return redirect("dashboard")
        else:
            messages.error(request, "⚠️ لطفاً خطاهای زیر را بررسی کنید.")

    return render(request, "users/force_password_change.html", {"form": form})