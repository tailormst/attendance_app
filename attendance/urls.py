from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('debug/', views.debug_view, name='debug'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('export/', views.export_report, name='export_report'),
]
