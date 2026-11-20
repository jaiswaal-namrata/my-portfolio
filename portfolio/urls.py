from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resume/', views.resume, name='resume'),
    path('dashboard/login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('dashboard/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/skills/add/', views.skill_create, name='skill_create'),
    path('dashboard/skills/<int:pk>/edit/', views.skill_edit, name='skill_edit'),
    path('dashboard/skills/<int:pk>/delete/', views.skill_delete, name='skill_delete'),
    path('dashboard/projects/add/', views.project_create, name='project_create'),
    path('dashboard/projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('dashboard/projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
]
