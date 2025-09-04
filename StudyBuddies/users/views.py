from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from study.models import StudySession, Subject
from study.forms import CreateSessionForm
from study.views import *
from datetime import *
from functools import reduce
from django.db.models import Sum
import json

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
 
    user_sessions = StudySession.objects.filter(user=request.user).order_by('-date')
    # Giornata
    today_hours = user_sessions.filter(date=datetime.now().date()) 
    hours_today_list = [t.duration for t in today_hours]
    hours_today_total = reduce(lambda tot, d: tot + d, hours_today_list, 0)
    
    # settimana
    start_week=datetime.now().date() - timedelta(days = 7)
    end_week = datetime.now().date() 
    weekly_hours = user_sessions.filter(date__range = (start_week, end_week))
    hours_weekly_list = [w.duration for w in weekly_hours]
    hours_weekly_total = reduce(lambda tot, d: tot + d, hours_weekly_list, 0)
    

    # Materia più studiata per la settimana
    favourite_subject = weekly_hours.values('subject__name').annotate(h = Sum('duration')).order_by('-h').first()

    # Dati grafico a torta
    today_subjects = user_sessions.filter(date=datetime.now().date()).values('subject__name').annotate(h=Sum('duration'))
    piechart_xvalues = [item['subject__name'] for item in today_subjects]
    piechart_yvalues = [float(item['h']) for item in today_subjects]
 
    # Dati grafico a linee
    line_graphx  = []
    line_graphy = []
    for i in range(6, -1, -1): 
        d = datetime.now().date() - timedelta(days = i)
        hour = user_sessions.filter(date=d).aggregate(total=Sum('duration'))['total'] or 0
        line_graphx.append(d.strftime('%d %m'))
        line_graphy.append(float(hour))




    context = {
        'hours_weekly_total': hours_weekly_total,
        'hours_today_total': hours_today_total,
        'favourite_subject': favourite_subject,
        'piechart_xvalues': json.dumps(piechart_xvalues),
        'piechart_yvalues': json.dumps(piechart_yvalues),
        'line_graphx': json.dumps(line_graphx),
        'line_graphy': json.dumps(line_graphy),
    }
    
    return render(request, "users/dashboard.html", context)

@login_required
def profile_view(request):

    return render(request, "users/profile.html")

    

