from django import forms
from .models import TouristSpot

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