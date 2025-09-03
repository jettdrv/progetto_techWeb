from django.urls import path
from . import views

app_name = 'study'

urlpatterns = [
    path('sessions/', views.study_session_list, name='session_list'),
    path('sessions/add/', views.study_session_create, name='add_session'),
    #path('sessions/<int:pk>/edit/', views.study_session_edit, name='session_edit'),
    #path('sessions/<int:pk>/delete/', views.study_session_delete, name='session_delete'),
    #path('statistics/', views.study_statistics, name='statistics'),
]