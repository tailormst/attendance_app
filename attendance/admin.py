from django.contrib import admin
from .models import UserProfile, Employee, Attendance


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number']
    search_fields = ['user__username', 'phone_number']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'emp_id', 'role', 'salary', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['name', 'emp_id', 'role']
    ordering = ['name']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'created_at']
    list_filter = ['status', 'date', 'employee']
    search_fields = ['employee__name', 'employee__emp_id']
    ordering = ['-date', 'employee']
