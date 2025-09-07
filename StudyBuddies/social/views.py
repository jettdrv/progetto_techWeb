from django.shortcuts import render, get_object_or_404, redirect
from .models import Friendship
from users.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.views import calculate_today_hours, calculate_week_hours
from study.models import StudySession

@login_required
def show_friend_list(request):
    friends = request.user.friends.all()
    for friend in friends:
        user_sessions = StudySession.objects.filter(user=friend)
        today_hours = calculate_today_hours(user_sessions)
        week_hours = calculate_week_hours(user_sessions)

        friend.today_hours = today_hours
        friend.week_hours = week_hours
    return render(request, 'social/friend_list.html', {'friends': friends})


@login_required
def user_search(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(
            Q(username__contains=query) 
        )

    for user in users:
        user.is_friend= request.user.is_friend_with(user)

    context={
        'users': users,
        'query': query,
        'results_count':users.count()
    }

    return render(request, 'social/user_search.html', context)

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)

    Friendship.objects.create(from_user = request.user, to_user = to_user, status='pending')
    messages.success(request, 'Richiesta di amicizia inviata')
    return redirect('social:user_search')

@login_required
def view_friend_requests(request):
    friend_requests = Friendship.objects.filter(to_user =request.user, status ='pending').select_related('from_user')
    return render(request, 'social/friend_requests.html', {'friend_requests':friend_requests})

@login_required
def accept_friend_request(request, friend_req_id):
    friend_request = get_object_or_404(Friendship, id = friend_req_id, to_user = request.user, status='pending')
    friend_request.accept()
    messages.success(request, 'Richiesta accettata')
    return redirect('social:friend_requests')

@login_required
def reject_friend_request(request, friend_req_id):
    friend_request = get_object_or_404(Friendship, id = friend_req_id, to_user = request.user, status='pending')
    friend_request.reject()
    messages.success(request, 'Richiesta rifiutata')
    return redirect('social:friend_requests')


@login_required
def remove_friend(request, user_id):
    friend_user = get_object_or_404(CustomUser, id=user_id)

    if request.user.remove_friend(friend_user):
        messages.success(request, 'Rimozione con successo')
    else:
        messages.info(request,'Non eravate amici')
    return redirect('social:friends')

