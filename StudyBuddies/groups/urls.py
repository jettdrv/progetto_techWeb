from django.urls import path, include
from . import views

app_name = 'groups'

urlpatterns = [

    path('', views.group_list, name="group_list"),
    path('create/', views.create_group, name="create_group"),
    path('<int:group_id>/', views.group_details, name="group_details"),
    path('<int:group_id>/join', views.join_public_group, name="join_group"),
    path('<int:group_id>/add_discussion', views.add_discussion, name="add_discussion"),
    path('<int:discussion_id>/add_comment', views.add_comment, name="add_comment"),
    path('<int:group_id>/invite/', views.group_invite, name='group_invite'),
    path('invite/<int:invite_id>/<str:action>/', views.invite_response, name='invite_response'),
    path('my-invites/', views.my_invites, name='my_invites'),
    path('<int:group_id>/manage/', views.group_manage, name='group_manage'),
    path('<int:group_id>/remove/<int:user_id>/', views.remove_member, name='remove_member'),
    path('discussion/<int:discussion_id>/delete/', views.delete_discussion, name='delete_discussion'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]