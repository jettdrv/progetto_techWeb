from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from study.models import StudySession
from study.forms import CreateSessionForm
from study.views import *

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("users:dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("homepage")

@login_required
def dashboard_view(request):
    study_session_create(request)  #form per la creazione di una sessione di studio definita in study.forms
    


    return render(request, "users/dashboard.html")

@login_required
def profile_view(request):

    return render(request, "users/profile.html")

    

