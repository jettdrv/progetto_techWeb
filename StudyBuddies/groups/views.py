from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def group_list(request):
    groups = StudyGroup.objects.filter(memberships__user = request.user)
    public_groups = StudyGroup.objects.filter(privacy = 'public').exclude(memberships__user = request.user)
    return render(request, 'groups/group_list.html', {'groups': groups, 'public_groups': public_groups})

@login_required
def group_details(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    discussions = group.discussions.all().order_by('-created_at')
    discussion_form = GroupDiscussionForm()
    comment_form = CommentForm()
    #is_member = group.members.filter(id=request.user.id).exists()
    context = {'group': group, 'discussions': discussions, 'discussion_form':discussion_form, 'comment_form':comment_form }#'is_member': is_member}
    return render(request, 'groups/group_details.html', context)

@login_required
def create_group(request):
    if request.method =='POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            GroupMembership.objects.create(group = group, user = request.user, role='owner')
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
