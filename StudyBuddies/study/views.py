from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import StudySession, Subject
from .forms import CreateSessionForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm 
from reportlab.lib import colors 
from io import BytesIO
from django.http import FileResponse

#--------------FUNZIONI DI SERVIZIO------------------------------------------
def filter_sessions(user, req):
    user_sessions = StudySession.objects.filter(user=user)
    if req.get('subjects'):
        user_sessions=user_sessions.filter(subject_id=req['subjects'])
    
    if req.get('date'):
        user_sessions=user_sessions.filter(date=req['date'])

    return user_sessions


#-------------View principali---------------------------------
@login_required
def study_session_list(request):
    user_sessions = filter_sessions(request.user, request.GET)
    context = {
        'sessions' : user_sessions,
        'subjects' : Subject.objects.filter(created_by=request.user)
    }
    return render(request, 'study/session_list.html', context)

@login_required
def export_list(request):
    user_sessions = filter_sessions(request.user, request.GET)
    num_sessions=user_sessions.count()
 
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height-50, f"Lista sessioni di studio di {request.user.username}")
    p.line(50, height - 100, width - 50, height - 100)
    p.setFont("Helvetica", 12)
    p.drawString(50, height- 150, f"Sessioni totali: {num_sessions}")
    i = 1
    w = 50
    h = height - 170
    for session in user_sessions:
        p.drawString( 50, h, f"{i}. {session.__str__()}")
        i = i + 1
        h = h - 20
 
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename ="liste_sessioni.pdf")



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
        form = CreateSessionForm(request.POST, instance=session, user=request.user)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request, 'Sessione aggiornata con successo!')
            return redirect('study:session_list')
    else:
        form = CreateSessionForm(instance=session, user=request.user)
   
    return render(request, 'study/session_form.html', {'form': form, 'title': 'Modifica sessione'})

