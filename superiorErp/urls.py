"""
URL configuration for superiorErp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from views import (
    home,
    login_view,
    student_login,
    teacher_login,
    staff_login,
    logout_view,
    student_register,
    teacher_register,
    staff_register,
)

urlpatterns = [
    # Home
    path("", home, name="home"),

    # Authentication
    path("login/", login_view, name="login"),
    path("login/student/", student_login, name="student_login"),
    path("login/teacher/", teacher_login, name="teacher_login"),
    path("login/staff/", staff_login, name="staff_login"),
    path("logout/", logout_view, name="logout"),

    # Registration
    path("register/student/", student_register, name="student_register"),
    path("register/teacher/", teacher_register, name="teacher_register"),
    path("register/staff/", staff_register, name="staff_register"),

    # Student Account (Dashboard, Profile)
    path("account/", include("accounts.urls")),

    # Admission
    path("admission/", include("admission.urls")),

    # Dashboards
    path("dashboard/", include("dashboards.urls")),

    # Admin
    path("admin/", admin.site.urls),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

