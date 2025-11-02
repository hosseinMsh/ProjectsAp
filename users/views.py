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
