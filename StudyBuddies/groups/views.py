from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from users.models import CustomUser

@login_required
def group_list(request):
    groups = StudyGroup.objects.filter(groupmembership__user = request.user).order_by('-created_at')
    public_groups = StudyGroup.objects.filter(privacy = 'public').exclude(groupmembership__user = request.user)
    return render(request, 'groups/group_list.html', {'groups': groups, 'public_groups': public_groups})

@login_required
def group_details(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    if group.privacy == 'private' and not group.is_member(request.user):
        messages.error(request, 'Questo gruppo è privato. Devi essere invitato per accedere.')
        return redirect('groups:group_list')
    discussions = group.discussions.all().order_by('-created_at')
    discussion_form = GroupDiscussionForm()
    comment_form = CommentForm()
    context = {'group': group, 'is_creator': group.creator==request.user, 'discussions': discussions, 'discussion_form':discussion_form, 'comment_form':comment_form }
    
    return render(request, 'groups/group_details.html', context)

@login_required
def create_group(request):
    if request.method =='POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            GroupMembership.objects.create(user = request.user, group = group, role='owner')
            messages.success(request, 'Gruppo creato')
            return redirect('groups:group_details', group_id =group.id)
    else:
        form = StudyGroupForm()

    return render(request, "groups/create_group.html", {'form':form})

@login_required
def add_discussion(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    if request.method =='POST':
        form = GroupDiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.group = group
            discussion.creator = request.user
            discussion.save()
        else:
            print(form.errors)
    return redirect("groups:group_details", group_id=group.id)

@login_required
def add_comment(request, discussion_id):
    discussion = get_object_or_404(GroupDiscussion, id = discussion_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.creator = request.user
            comment.save()
    return redirect("groups:group_details", group_id= discussion.group.id)

@login_required
def group_invite(request, group_id):
    group = get_object_or_404(StudyGroup, id = group_id)

    if not group.is_creator(request.user):
        messages.error(request, 'Solo il creatore del gruppo può invitare utenti.')
        return redirect('groups:group_detail', group_id=group.id)
    
    if group.privacy != 'private':
        messages.error(request, 'Puoi invitare utenti solo in gruppi privati.')
        return redirect('groups:group_detail', group_id=group.id)
    
    if request.method == 'POST':
        form = GroupInviteForm(request.POST)
        if form.is_valid():
            invitee = form.cleaned_data['username']
            if group.is_member(invitee):
                messages.error(request, f'{invitee.username} è già membro del gruppo.')
            elif GroupInvite.objects.filter(group=group, invitee=invitee, status='pending').exists():
                messages.error(request, f'{invitee.username} ha già un invito pendente.')
            else:
                GroupInvite.objects.create(group=group, inviter=request.user, invitee=invitee)
                messages.success(request, f'Invito inviato a {invitee.username}!')
            
            return redirect('groups:group_invite', group_id=group.id)
    else:
        form = GroupInviteForm()

    pending_invites = group.invites.filter(status='pending')
    
    context = {'group': group,'form': form,'pending_invites': pending_invites
    }
    return render(request, 'groups/group_invite.html', context)

@login_required
def invite_response(request, invite_id, action):
    invite = get_object_or_404(GroupInvite, id=invite_id, invitee=request.user)
    if action == 'accept':
        invite.accept()
        messages.success(request, f'Ti sei unito al gruppo "{invite.group.name}"!')
    elif action == 'reject':
        invite.reject()
        messages.info(request, f'Hai rifiutato l\'invito a "{invite.group.name}".')
    else:
        messages.error(request, 'Azione non valida.')
    
    return redirect('groups:group_list')

@login_required
def my_invites(request):
    invites = GroupInvite.objects.filter(invitee=request.user, status='pending')
    return render(request, 'groups/my_invites.html', {'invites': invites})

@login_required
def group_manage(request, group_id):
    group = get_object_or_404(StudyGroup, id = group_id)
    if not group.creator == request.user:
        messages.error(request, "Solo l'utente creatore puo modificare il gruppo")
        return redirect('groups:group_detail', group_id = group.id)
    
    members = GroupMembership.objects.filter(group = group).exclude(user = group.creator)
    return render(request, 'groups/group_manage.html', {'group':group , 'members' : members})

@login_required
def remove_member(request, group_id, user_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    user_remove=get_object_or_404(CustomUser, id=user_id)

    if not group.creator == request.user:
        messages.error(request, "Solo l'utente creatore puo espellere i membri")
        return redirect('groups:group_detail', group_id = group.id)
    
    if user_remove == request.user:
        messages.error(request, "Non puoi rimuovere te stesso")
        return redirect('groups:group_manage', group_id = group.id)
    
    if not group.is_member(user_remove):
        messages.error(request, "Membro non presente nel gruppo")
        return redirect('groups:group_manage', group_id = group.id)
    
    GroupMembership.objects.filter(user=user_remove, group=group).delete()
    messages.success(request, 'Utente rimosso con successo')
    return redirect('groups:group_manage', group_id=group.id)
  
@login_required
def delete_discussion(request, discussion_id):
    discussion = get_object_or_404(GroupDiscussion, id=discussion_id)
    group = discussion.group

    if not (discussion.creator == request.user or group.creator == request.user):
        messages.error(request, 'Non puoi rimuovere questa discussione')
        return redirect('groups:group_detail', group_id=group.id)
    
    if request.method == 'POST':
        group_id = discussion.group.id
        discussion.delete()
        messages.success(request, 'Discussione eliminata.')
        return redirect('groups:group_details', group_id=group_id)
    
    return render(request, 'groups/delete_confirm.html', {
        'object': discussion,
        'message': f'Sei sicuro di voler eliminare la discussione "{discussion.title}"?'
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    group = comment.discussion.group

    if not (comment.creator == request.user or group.creator == request.user):
        messages.error(request, 'Non puoi eliminare questo commento')
        return redirect('groups:group_detail', group_id=group.id)
    
    if request.method == 'POST':
        discussion_id = comment.discussion.id
        comment.delete()
        messages.success(request, 'Commento eliminato.')
        return redirect('groups:group_details', group_id=group.id)
    
    return render(request, 'groups/delete_confirm.html', {
        'object': comment,
        'message': 'Sei sicuro di voler eliminare questo commento?'
    })