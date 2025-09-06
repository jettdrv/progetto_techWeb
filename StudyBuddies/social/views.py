from django.shortcuts import render, get_object_or_404, redirect
from .models import Friendship
from users.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def show_friend_list(request):
    friends = request.user.friends.all()

    return render(request, 'social/friend_list.html', {'friends': friends})


@login_required
def add_friend(request, user_id):
    friend_user = get_object_or_404(CustomUser, id=user_id)

    if request.user != friend_user:
        request.user.add_friend(friend_user)
        messages.success(request, 'Richiesta inviata')
    else:
        messages.success(request, 'Non puoi aggiungerti come amico da solo')
    return redirect('social:friends')

@login_required
def remove_friend(request, user_id):
    friend_user = get_object_or_404(CustomUser, id=user_id)

    if request.user.remove_friend(friend_user):
        messages.success(request, 'Rimozione con successo')
    else:
        messages.info(request, f"Non eri amico di {friend_user.username}")
    return redirect('social:friends')



@login_required
def user_search(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(
            Q(username__contains=query) |
            Q(email__contains=query)|
            Q(expertise_field__contains=query)
        )

    for user in users:
        user.is_friend= request.user.is_friend_with(user)

    context={
        'users': users,
        'query': query,
        'results_count':users.count()
    }

    return render(request, 'social/user_search.html', context)


#da implementare le richieste di amicizia
#def send_friend_request(request):
#def accept_friend_request(request):
#def reject_friend_request(request):
