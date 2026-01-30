from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from . import views

def logout_view(request):
    """Custom logout view with message"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('landing')

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.update_profile, name='profile_edit'),
    path('api/profile/toggle-availability/', views.toggle_availability, name='toggle_availability'),
]

