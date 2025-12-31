from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage, StudyTourBooking
import re

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('', '-- Select Department --'),
        ('cse', 'CSE'),
        ('bba', 'BBA'),
        ('llb', 'LLB'),
        ('english', 'English'),
    ]
    
    # Common fields
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    
    # Student specific fields
    student_id = forms.CharField(max_length=20, required=False)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=False)
    session = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=15, required=False)
    
    # Admin specific fields (NO DEPARTMENT FOR ADMIN)
    employee_id = forms.CharField(max_length=20, required=False)
    designation = forms.CharField(max_length=100, required=False)
    admin_phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'role', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        if role == 'student':
            # Student validation
            if not cleaned_data.get('student_id'):
                raise forms.ValidationError("Student ID is required for students.")
            if not cleaned_data.get('department'):
                raise forms.ValidationError("Department is required for students.")
            if not cleaned_data.get('session'):
                raise forms.ValidationError("Session is required for students.")
            
            # Phone is optional for students, no validation needed
            
        elif role == 'admin':
            # Admin validation (NO DEPARTMENT FOR ADMIN)
            if not cleaned_data.get('employee_id'):
                raise forms.ValidationError("Employee ID is required for admins.")
            if not cleaned_data.get('designation'):
                raise forms.ValidationError("Designation is required for admins.")
            if not cleaned_data.get('admin_phone'):
                raise forms.ValidationError("Phone number is required for admins.")
            
            # Validate admin phone format
            phone = cleaned_data.get('admin_phone')
            if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
                raise forms.ValidationError("Enter a valid phone number.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # Store additional user information
            user.first_name = self.cleaned_data['name']
            
            # Store role information in last_name field temporarily
            user.last_name = f"Role: {self.cleaned_data['role']}"
            
            user.save()
            
        return user


class StudyTourBookingForm(forms.ModelForm):
    class Meta:
        model = StudyTourBooking
        fields = ['study_tour', 'tour_date', 'special_requirements']
        widgets = {
            'study_tour': forms.HiddenInput(),
            'special_requirements': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Any special requirements or dietary restrictions...'
            }),
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number (optional)'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Tell us about your inquiry...',
                'required': True
            }),
        }