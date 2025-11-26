from django.urls import path
from . import views

urlpatterns = [
    # Student Login & Dashboard
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/edit/', views.student_profile_edit, name='student_profile_edit'),
    path('logout/', views.student_logout, name='student_logout'),
]

