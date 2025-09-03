from django.urls import path
from . import views

app_name = 'study'

urlpatterns = [
    path('sessions/', views.study_session_list, name='session_list'),
    path('sessions/add/', views.study_session_create, name='add_session'),
    path('sessions/<int:pk>/delete/', views.delete_study_session, name='delete_session'),
    path('sessions/<int:pk>/edit/', views.edit_study_session, name='edit_session'),
    
    #path('statistics/', views.study_statistics, name='statistics'),
]