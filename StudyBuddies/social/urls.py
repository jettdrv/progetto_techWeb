from django.urls import path, include
from . import views

app_name = 'social'

urlpatterns = [

    path('search/', views.user_search, name="user_search"),
    path('friend-list/', views.show_friend_list, name="friends"),
    path('friend-list/remove/<int:user_id>/', views.remove_friend, name="remove_friend"),
    path('friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friend-requests/', views.view_friend_requests, name='friend_requests'),
    path('friend-request/<int:friend_req_id>/accept/', views.accept_friend_request, name='accept_friend_request'),
    path('friend-request/<int:friend_req_id>/reject/', views.reject_friend_request, name='reject_friend_request'),
    
    
]