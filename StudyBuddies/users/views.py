from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .forms import CustomUserCreationForm, ProfilePictureForm, GoalSettingsForm
from study.models import StudySession, Subject
from study.forms import CreateSessionForm
from study.views import *
from datetime import *
from functools import reduce
from django.db.models import Sum
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm 
from reportlab.lib import colors 
from io import BytesIO
import os

#-------------------------FUNZIONI DI SERVIZIO---------------------------------
def calculate_day_hours(sessions, day):
    day_sessions = sessions.filter(date=day)
    day_hours = day_sessions.aggregate(total=Sum('duration'))['total'] or 0
    return day_hours

def calculate_today_hours(sessions):
    day = datetime.today().date()
    today_hours = calculate_day_hours(sessions, day)
    return today_hours

def weekly_hours(sessions):
    start_week=datetime.now().date() - timedelta(days = 7)
    end_week = datetime.now().date() 
    weekly_h = sessions.filter(date__range = (start_week, end_week))
    return weekly_h

def calculate_week_hours(sessions):
    weekly_h = weekly_hours(sessions)
    hours_weekly_list = [w.duration for w in weekly_h]
    hours_weekly_total = reduce(lambda tot, d: tot + d, hours_weekly_list, 0)
    return hours_weekly_total

def most_studied(sessions):
    weekly_h = weekly_hours(sessions)
    fav_subject = weekly_h.values('subject__name').annotate(h = Sum('duration')).order_by('-h').first()
    return fav_subject


def daily_goal_progress(user, sessions):
    today_hours = calculate_today_hours(sessions)

    return {
        'current': today_hours,
        'target': user.daily_goal_hours,
        'percentage': min(100, (float(today_hours) / float(user.daily_goal_hours)) * 100) if user.daily_goal_hours > 0 else 0,
        'completed': today_hours >= user.daily_goal_hours
    }
def goal_progress_any_day(user, sessions, day):
    day_hours = calculate_day_hours(sessions, day)
    return {
        'current': day_hours,
        'target': user.daily_goal_hours,
        'percentage': min(100, (float(day_hours) / float(user.daily_goal_hours)) * 100) if user.daily_goal_hours > 0 else 0,
        'completed': day_hours >= user.daily_goal_hours
    }

    
def weekly_goal_progress(user, sessions):
    weekly_hours = calculate_week_hours(sessions)
        
    return {
        'current': weekly_hours,
        'target': user.weekly_goal_hours,
        'percentage': min(100, (float(weekly_hours) / float(user.weekly_goal_hours)) * 100) if user.weekly_goal_hours > 0 else 0,
        'completed': weekly_hours >= user.weekly_goal_hours
    }

def streak(user, sessions):
    streak = 0;
    today = datetime.today().date()
    for i in range(365):
        day = today - timedelta(days=i)
        print(day)
        if goal_progress_any_day(user, sessions, day)['completed']:
            streak = streak + 1
        else:
            break
    return streak


#--------------------View DASHBOARD----------------------------------------------
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
    hours_today_total = calculate_today_hours(user_sessions)
    # settimana
    hours_weekly_total = calculate_week_hours(user_sessions)
    # Materia più studiata per la settimana
    favourite_subject = most_studied(user_sessions)
    #streak
    streak_count = streak(request.user, user_sessions)

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
    #dati grafici obiettivi
    daily = daily_goal_progress(request.user, user_sessions)
    weekly = weekly_goal_progress(request.user, user_sessions)
    
    context = {
        'hours_weekly_total': hours_weekly_total,
        'hours_today_total': hours_today_total,
        'favourite_subject': favourite_subject,
        'streak_count': streak_count,
        'piechart_xvalues': json.dumps(piechart_xvalues),
        'piechart_yvalues': json.dumps(piechart_yvalues),
        'line_graphx': json.dumps(line_graphx),
        'line_graphy': json.dumps(line_graphy),
        'daily_current': json.dumps(float(daily['current'])),
        'daily_remaining': json.dumps(float(max(daily['target'] - daily['current'], 0))),
        'weekly_current': json.dumps(float(weekly['current'])),
        'weekly_remaining': json.dumps(float(max(weekly['target'] - weekly['current'] , 0))),
    }
    return render(request, "users/dashboard.html", context)

@login_required
def set_goal(request):

    if request.method=='POST':
        form = GoalSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'obiettivo aggiunto')
            return redirect('users:profile')
        
    else:
        form = GoalSettingsForm(instance=request.user)
    return render(request, 'users/set_goal.html', {'form':form})


@login_required
def profile_view(request):

    return render(request, "users/profile.html")


@login_required
def export_pdf(request):
    #calcolo i dati principali nel dashboard da includere nel report
    user_sessions= StudySession.objects.filter(user=request.user)
    date_today= (datetime.now().date()).strftime('%d %m %Y')
    first_day_week = (datetime.now().date() - timedelta(days=7)).strftime('%d %m %Y')
    ore_oggi = calculate_today_hours(user_sessions)

    ore_settimana = calculate_week_hours(user_sessions)

    sub = most_studied(user_sessions)['subject__name']
    streak_count = streak(request.user, user_sessions)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(150, height-50, f"Riepilogo per {request.user.username}")
    p.line(50, height - 100, width - 50, height - 100)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height-120, "Ore totali per oggi")
    p.setFont("Helvetica", 12)
    p.drawString(230, height-120, f"-({date_today}) : {ore_oggi}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height-140, "Ore totali per questa settimana")
    p.setFont("Helvetica", 12)
    p.drawString(230, height-140, f"-({first_day_week}-{date_today}) : {ore_settimana}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height-160, "Materia più studiata")
    p.setFont("Helvetica", 12)
    p.drawString(230, height-160, f"-({first_day_week}-{date_today}) : {sub}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height-180, "Giorni consecutivi")
    p.setFont("Helvetica", 12)
    p.drawString(230, height-180, f"- : {streak_count}")


    #da implementare altre statistiche come la media settimanale
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename ="report_studio.pdf")

@login_required
def profile_picture_update(request):
    if request.method =='POST':

        form = ProfilePictureForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Immagine profilo cambiata con successo')
            return redirect('users:profile')
        else:
            messages.error(request, 'errore' + str(form.errors))
    else:
        form = ProfilePictureForm(instance=request.user)
    return render(request, 'users/updatePFP.html', {'form':form})

@login_required
def profile_picture_delete(request):
    user = request.user
    
    if request.method == 'POST':
        if user.profile_picture and user.profile_picture != '/pfp/nopfp.jpg':
            if os.path.isfile(user.profile_picture.path):
                os.remove(user.profile_picture.path)

            user.profile_picture='/pfp/nopfp.jpg'
            user.save()

            messages.success(request, 'immagine di profilo rimossa')
        else:
            messages.info(request, 'non hai una immagine di profilo')
        return redirect('users:profile')
    return render(request, 'users/deletePFP.html')

