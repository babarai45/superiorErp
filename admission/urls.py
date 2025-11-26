from django.urls import path
from . import views

urlpatterns = [
    path('', views.admission_main, name='admission_main'),
    path('start/', views.start_application, name='start_application'),
    path('start/<str:program_code>/', views.start_application, name='start_application_with_program'),
    path('login/', views.admission_login, name='admission_login'),

    path('stage1/<str:app_id>/', views.admission_stage1, name='admission_stage1'),
    path('stage2/<str:app_id>/', views.admission_stage2, name='admission_stage2'),
    path('stage3/<str:app_id>/', views.admission_stage3, name='admission_stage3'),
    path('stage4/<str:app_id>/', views.admission_stage4, name='admission_stage4'),
    path('stage5/<str:app_id>/', views.admission_stage5, name='admission_stage5'),
    path('confirmation/<str:app_id>/', views.admission_confirmation, name='admission_confirmation'),
]

