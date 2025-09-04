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
    
    return render(request, 'study/session_list.html', {"sessions" : sessions})

@login_required
def study_session_create(request):
    if request.method == 'POST':
        form = CreateSessionForm(request.POST, user=request.user)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            messages.success(request, 'Sessione di studio aggiunta con successo!')
            return redirect('study:session_list')
    else:
        form = CreateSessionForm(user=request.user)
    
    return render(request, 'study/session_form.html', {'form': form, 'title': 'Aggiungi Sessione'})

@login_required
def delete_study_session(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'Sessione eliminata con successo!')
        return redirect('study:session_list')
    
    return redirect('study:session_list')


@login_required
def edit_study_session(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = CreateSessionForm(request.POST, instance=session)
        if form.is_valid():
            print(form.cleaned_data)
            form.save(commit=False)
            messages.success(request, 'Sessione aggiornata con successo!')
            return redirect('study:session_list')
    else:
        form = CreateSessionForm(instance=session)
   
    return render(request, 'study/session_form.html', {'form': form, 'title': 'Modifica sessione'})

