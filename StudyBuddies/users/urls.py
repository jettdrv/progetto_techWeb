from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('profile/', views.profile_view, name="profile"),
    path('export-pdf/', views.export_pdf, name="export"),
    path('profile/updatePFP/', views.profile_picture_update, name="update_pfp"),
    path('profile/deletePFP/', views.profile_picture_delete, name="delete_pfp"),


]