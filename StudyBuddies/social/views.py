from django.shortcuts import render, get_object_or_404, redirect
from .models import Friendship
from users.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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

#def send_friend_request(request):
#def accept_friend_request(request):
#def reject_friend_request(request):



