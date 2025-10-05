from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, date
import csv
import json

from .models import Employee, Attendance, UserProfile
from .forms import CustomUserCreationForm, EmployeeForm, AttendanceForm


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number', '')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Basic validation
        if not username or not password1 or not password2:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'registration/clean_register.html')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'registration/clean_register.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'registration/clean_register.html')
        
        try:
            from django.contrib.auth.models import User
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'registration/clean_register.html')
            
            # Create user
            user = User.objects.create_user(username=username, password=password1)
            
            # Create UserProfile
            from .models import UserProfile
            UserProfile.objects.create(user=user, phone_number=phone_number)
            
            # Login user
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'registration/clean_register.html')
    
    return render(request, 'registration/clean_register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'registration/clean_login.html')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Account is disabled.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/clean_login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def debug_view(request):
    """Debug view to check authentication status"""
    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None,
        'user_id': request.user.id if request.user.is_authenticated else None,
    })


@login_required
def dashboard(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('dashboard')
    else:
        form = EmployeeForm()
    
    context = {
        'employees': employees,
        'form': form,
    }
    return render(request, 'dashboard.html', context)


@login_required
def mark_attendance(request):
    employees = Employee.objects.all()
    selected_date = request.GET.get('date', timezone.now().date())
    
    if request.method == 'POST':
        date = request.POST.get('date')
        if not date:
            messages.error(request, 'Please select a date.')
            return redirect('mark_attendance')
        
        # Get existing attendance for the date
        existing_attendance = {att.employee.id: att for att in Attendance.objects.filter(date=date)}
        
        for employee in employees:
            status = request.POST.get(f'employee_{employee.id}')
            if status:
                try:
                    attendance, created = Attendance.objects.get_or_create(
                        employee=employee,
                        date=date,
                        defaults={'status': status}
                    )
                    if not created:
                        attendance.status = status
                        attendance.save()
                except Exception as e:
                    messages.error(request, f'Error saving attendance for {employee.name}: {str(e)}')
                    continue
        
        messages.success(request, f'Attendance marked successfully for {date}!')
        return redirect('mark_attendance')
    
    # Get attendance for selected date
    attendance_data = {}
    if selected_date:
        attendance_records = Attendance.objects.filter(date=selected_date)
        attendance_data = {att.employee.id: att.status for att in attendance_records}
    
    context = {
        'employees': employees,
        'selected_date': selected_date,
        'attendance_data': attendance_data,
    }
    return render(request, 'clean_mark_attendance.html', context)


@login_required
def attendance_report(request):
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    
    # Get all employees
    employees = Employee.objects.all()
    
    # Calculate attendance summary
    summary_data = []
    for employee in employees:
        # Get attendance records for the month
        attendance_records = Attendance.objects.filter(
            employee=employee,
            date__year=year,
            date__month=month
        )
        
        # Count statuses
        status_counts = attendance_records.values('status').annotate(count=Count('status'))
        status_dict = {item['status']: item['count'] for item in status_counts}
        
        present = status_dict.get('Present', 0)
        absent = status_dict.get('Absent', 0)
        leave = status_dict.get('Leave', 0)
        holiday = status_dict.get('Holiday', 0)
        
        total_days = present + absent + leave + holiday
        percentage = (present / total_days * 100) if total_days > 0 else 0
        
        summary_data.append({
            'employee': employee,
            'present': present,
            'absent': absent,
            'leave': leave,
            'holiday': holiday,
            'total_days': total_days,
            'percentage': round(percentage, 2)
        })
    
    # Prepare chart data
    chart_data = {
        'labels': [emp['employee'].name for emp in summary_data],
        'present': [emp['present'] for emp in summary_data],
        'absent': [emp['absent'] for emp in summary_data],
        'leave': [emp['leave'] for emp in summary_data],
    }
    
    context = {
        'summary_data': summary_data,
        'chart_data': json.dumps(chart_data),
        'month': int(month),
        'year': int(year),
    }
    return render(request, 'clean_attendance_report.html', context)


@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    
    # Get attendance records for the month
    attendance_records = Attendance.objects.filter(
        employee=employee,
        date__year=year,
        date__month=month
    ).order_by('date')
    
    context = {
        'employee': employee,
        'attendance_records': attendance_records,
        'month': int(month),
        'year': int(year),
    }
    return render(request, 'employee_detail.html', context)


@login_required
def export_report(request):
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    
    # Get all employees
    employees = Employee.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_report_{year}_{month}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee Name', 'Employee ID', 'Present Days', 'Absent Days', 'Leave Days', 'Holiday Days', 'Total Days', 'Attendance %'])
    
    for employee in employees:
        attendance_records = Attendance.objects.filter(
            employee=employee,
            date__year=year,
            date__month=month
        )
        
        status_counts = attendance_records.values('status').annotate(count=Count('status'))
        status_dict = {item['status']: item['count'] for item in status_counts}
        
        present = status_dict.get('Present', 0)
        absent = status_dict.get('Absent', 0)
        leave = status_dict.get('Leave', 0)
        holiday = status_dict.get('Holiday', 0)
        
        total_days = present + absent + leave + holiday
        percentage = (present / total_days * 100) if total_days > 0 else 0
        
        writer.writerow([
            employee.name,
            employee.emp_id,
            present,
            absent,
            leave,
            holiday,
            total_days,
            f"{percentage:.2f}%"
        ])
    
    return response
