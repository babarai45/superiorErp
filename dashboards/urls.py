from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/courses/', views.student_courses, name='student_courses'),
    path('student/course/<int:course_id>/', views.course_details, name='course_details'),
    path('student/attendance/', views.student_attendance, name='student_attendance'),
    path('student/grades/', views.student_grades, name='student_grades'),

    # Teacher URLs
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/course/<int:course_id>/students/', views.teacher_course_students, name='teacher_course_students'),
    path('teacher/course/<int:course_id>/assessments/', views.teacher_assessments, name='teacher_assessments'),
    path('teacher/course/<int:course_id>/attendance/', views.teacher_attendance, name='teacher_attendance'),

    # Admin URLs
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/approvals/<str:user_type>/', views.admin_approvals, name='admin_approvals'),
    path('admin/approve/<str:user_type>/<int:user_id>/', views.approve_user, name='approve_user'),
]

