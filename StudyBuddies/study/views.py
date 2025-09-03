from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import StudySession
from .forms import CreateSessionForm

@login_required
def study_session_list(request):
    sessions = StudySession.objects.filter(user=request.user).select_related('user')
    '''
    # Filtri
    subject_filter = request.GET.get('subject')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if subject_filter and subject_filter != 'all':
        sessions = sessions.filter(subject__id=subject_filter)
    
    if date_from:
        sessions = sessions.filter(date__gte=date_from)
    
    if date_to:
        sessions = sessions.filter(date__lte=date_to)
    
    subjects = Subject.objects.all().order_by('name')
    
    context = {
        'sessions': sessions,
        'subjects': subjects,
        'total_hours': sessions.aggregate(total=Sum('duration'))['total'] or 0,
    }
    '''
    return render(request, 'study/session_list.html', {"sessions" : sessions})

@login_required
def study_session_create(request):
    if request.method == 'POST':
        form = CreateSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            messages.success(request, 'Sessione di studio aggiunta con successo!')
            return redirect('study:session_list')
    else:
        form = CreateSessionForm()
    
    return render(request, 'study/session_form.html', {'form': form, 'title': 'Aggiungi Sessione'})
'''
@login_required
def study_session_edit(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = StudySessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sessione aggiornata con successo!')
            return redirect('study:session_list')
    else:
        form = StudySessionForm(instance=session)
    
    return render(request, 'study/session_form.html', {'form': form, 'title': 'Modifica Sessione'})

@login_required
def study_session_delete(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'Sessione eliminata con successo!')
        return redirect('study:session_list')
    
    return render(request, 'study/session_confirm_delete.html', {'session': session})

@login_required
def study_statistics(request):
    # Statistiche generali
    total_sessions = StudySession.objects.filter(user=request.user).count()
    total_hours = StudySession.objects.filter(user=request.user).aggregate(
        total=Sum('duration')
    )['total'] or 0
    
    # Statistiche settimanali
    week_ago = timezone.now().date() - timedelta(days=7)
    weekly_hours = StudySession.objects.filter(
        user=request.user, 
        date__gte=week_ago
    ).aggregate(total=Sum('duration'))['total'] or 0
    
    # Statistiche giornaliere
    today_hours = StudySession.objects.filter(
        user=request.user, 
        date=timezone.now().date()
    ).aggregate(total=Sum('duration'))['total'] or 0
    
    # Materia più studiata
    favorite_subject = StudySession.objects.filter(
        user=request.user
    ).values('subject__name').annotate(
        total_hours=Sum('duration')
    ).order_by('-total_hours').first()
    
    # Distribuzione per materia (per grafico a torta)
    subject_distribution = StudySession.objects.filter(
        user=request.user
    ).values('subject__name').annotate(
        hours=Sum('duration')
    ).order_by('-hours')
    
    # Trend settimanale (per grafico a linee)
    dates = []
    hours_per_day = []
    
    for i in range(6, -1, -1):  # Ultimi 7 giorni
        date = timezone.now().date() - timedelta(days=i)
        daily_hours = StudySession.objects.filter(
            user=request.user, 
            date=date
        ).aggregate(total=Sum('duration'))['total'] or 0
        
        dates.append(date.strftime('%d/%m'))
        hours_per_day.append(float(daily_hours))
    
    context = {
        'total_sessions': total_sessions,
        'total_hours': total_hours,
        'weekly_hours': weekly_hours,
        'today_hours': today_hours,
        'favorite_subject': favorite_subject,
        'subject_distribution': subject_distribution,
        'dates': dates,
        'hours_per_day': hours_per_day,
    }
    return render(request, 'study/statistics.html', context)
    '''