from django.urls import path, include
from . import views

app_name = 'groups'

urlpatterns = [

    path('', views.group_list, name="group_list"),
    path('create/', views.create_group, name="create_group"),
    path('<int:group_id>/', views.group_details, name="group_details"),
    path('<int:group_id>/add_discussion', views.add_discussion, name="add_discussion"),
    path('<int:discussion_id>/add_comment', views.add_comment, name="add_comment"),
    
]