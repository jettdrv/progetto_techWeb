from django.shortcuts import render, get_object_or_404, redirect
from .models import Friendship
from users.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.views import calculate_today_hours, calculate_week_hours
from study.models import StudySession
from .forms import SearchForm
from groups.models import StudyGroup

@login_required
def show_friend_list(request):
    friends = request.user.friends_accepted
    for friend in friends:
        user_sessions = StudySession.objects.filter(user=friend)
        today_hours = calculate_today_hours(user_sessions)
        week_hours = calculate_week_hours(user_sessions)

        friend.today_hours = today_hours
        friend.week_hours = week_hours
    return render(request, 'social/friend_list.html', {'friends': friends})


@login_required
def search_user_or_group(request):
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data.get('search_string')
            search_from = form.cleaned_data.get('search_from')
            return redirect('social:search_results', search_string=search_string, search_from = search_from)
    else:
        form = SearchForm()
    
    return render(request, 'social/user_search.html', {'form':form})

@login_required
def search_results(request, search_string, search_from):
    results =None;
    if search_from=='users':
        results = CustomUser.objects.filter(username__icontains=search_string).exclude(id=request.user.id)
        for u in results:
            u.is_friend=request.user.is_friend_with(u)
            if not u.is_friend:
                u.friend_request_status = request.user.friend_request_status(u)
    elif search_from=='groups':
        results = StudyGroup.objects.filter(name__icontains=search_string)
        results = results.filter(privacy='public')
    context={'search_string':search_string,'search_from':search_from, 'results':results}
    return render(request, "social/search_results.html", context)

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)
    existing_friendship = Friendship.objects.filter(Q(from_user=request.user, to_user=to_user)|Q(from_user=to_user, to_user=request.user)).first()
    
    if existing_friendship:
        if existing_friendship.status=='pending':
            messages.error(request, 'richiesta gia inviata')
        elif existing_friendship.status=='accepted':
            messages.info(request, 'siete gia amici')
        else:
            messages.info(request, 'richiesta gia gestita')
        return redirect('social:search')
           
    Friendship.objects.create(from_user = request.user, to_user = to_user, status='pending')
    messages.success(request, 'Richiesta di amicizia inviata')
    return redirect('social:search')

@login_required
def view_friend_requests(request):
    accepted_friends = request.user.friends_accepted

    friend_requests =Friendship.objects.filter(
        to_user=request.user, 
        status='pending'
    ).exclude(
        from_user__in=accepted_friends
    ).select_related('from_user')
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

    if request.user.is_friend_with(friend_user):
        request.user.remove_friend(friend_user)
        messages.success(request, 'Rimozione con successo')
    else:
        messages.info(request,'Non eravate amici')
    return redirect('social:friends')

