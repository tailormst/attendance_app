from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, Attendance


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, 
        required=False, 
        help_text='Optional.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create UserProfile
            from .models import UserProfile
            UserProfile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'emp_id', 'role', 'salary']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_id': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class AttendanceForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=lambda: forms.DateField().widget.attrs.get('value', '')
    )
    
    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees', None)
        super().__init__(*args, **kwargs)
        
        if employees:
            for employee in employees:
                self.fields[f'employee_{employee.id}'] = forms.ChoiceField(
                    choices=Attendance.STATUS_CHOICES,
                    widget=forms.Select(attrs={'class': 'form-select'}),
                    label=employee.name,
                    required=False
                )
