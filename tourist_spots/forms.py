from django import forms
from .models import TouristSpot, TourPackage, PackageBooking, Payment

class TouristSpotForm(forms.ModelForm):
    class Meta:
        model = TouristSpot
        fields = ['name', 'description', 'image', 'highlights', 'travel_info', 'best_time', 'safety_info']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter spot name',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Enter description',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical;'
            }),
            'highlights': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Enter highlights (one per line)',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical;'
            }),
            'travel_info': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Enter travel information',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical;'
            }),
            'best_time': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter best time to visit',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical;'
            }),
            'safety_info': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter safety information',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical;'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            })
        }


class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ['name', 'description', 'image', 'price', 'duration', 'destination', 'highlights', 'category', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter package name',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Enter package description',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical;'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter price (e.g., 5000)',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., 3 Days 2 Nights',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter destination',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'highlights': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter highlights (one per line)',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical;'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 8px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 20px; height: 20px;'
            })
        }


class PackageBookingForm(forms.ModelForm):
    class Meta:
        model = PackageBooking
        fields = ['student_name', 'student_id', 'department', 'semester', 'phone', 'email', 'emergency_contact', 'num_persons', 'special_requests']
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your full name',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your Student ID',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Computer Science',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., 5th Semester',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your phone number',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your email address',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Emergency contact number (optional)',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'num_persons': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 1,
                'max': 10,
                'value': 1,
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Any special requests or requirements (optional)',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical;'
            }),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_paid', 'bkash_last_4']
        widgets = {
            'amount_paid': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter amount paid',
                'type': 'number',
                'step': '0.01',
                'min': '0',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'bkash_last_4': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Last 4 digits of bKash number',
                'maxlength': '4',
                'pattern': '[0-9]{4}',
                'style': 'width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        amount_paid = cleaned_data.get('amount_paid')
        bkash_last_4 = cleaned_data.get('bkash_last_4')
        
        if amount_paid and amount_paid <= 0:
            raise forms.ValidationError('Amount must be greater than 0.')
        
        if bkash_last_4 and (not bkash_last_4.isdigit() or len(bkash_last_4) != 4):
            raise forms.ValidationError('bKash number must be exactly 4 digits.')
        
        return cleaned_data