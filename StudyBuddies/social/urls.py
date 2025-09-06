from django.urls import path, include
from . import views

app_name = 'social'

urlpatterns = [

    path('search/', views.user_search, name="user_search"),
    path('friend-list/', views.show_friend_list, name="friends"),
    path('friend-list/add/<int:user_id>', views.add_friend, name="add_friend"),
    path('friend-list/remove/<int:user_id>/', views.remove_friend, name="remove_friend"),
    
]