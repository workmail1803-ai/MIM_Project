from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import OperationalError
from django.contrib.auth.forms import UserCreationForm
from .models import TouristSpot
from .forms import TouristSpotForm

def home(request):
    try:
        spots = TouristSpot.objects.all()
    except OperationalError:
        # If database table doesn't exist yet, show empty spots
        spots = []
        messages.warning(request, "Database is being set up. Please wait a moment and refresh.")
    
    return render(request, 'home.html', {'spots': spots})

@login_required
def add_tourist_spot(request):
    if request.method == 'POST':
        form = TouristSpotForm(request.POST, request.FILES)
        if form.is_valid():
            spot = form.save(commit=False)
            spot.created_by = request.user
            spot.save()
            messages.success(request, f'"{spot.name}" has been added successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TouristSpotForm()
    
    return render(request, 'add_spot.html', {'form': form})

def spot_detail(request, spot_id):
    spot = get_object_or_404(TouristSpot, id=spot_id)
    return render(request, 'spot_detail.html', {'spot': spot})

def packages(request):
    return render(request, 'packages.html')

def travel_history(request):
    return render(request, 'travel_history.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import TouristSpot
from .forms import TouristSpotForm

def home(request):
    spots = TouristSpot.objects.all()
    return render(request, 'home.html', {'spots': spots})

@login_required
def add_tourist_spot(request):
    if request.method == 'POST':
        form = TouristSpotForm(request.POST, request.FILES)
        if form.is_valid():
            spot = form.save(commit=False)
            spot.created_by = request.user
            spot.save()
            messages.success(request, f'"{spot.name}" has been added successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TouristSpotForm()
    
    return render(request, 'add_spot.html', {'form': form})

def spot_detail(request, spot_id):
    spot = get_object_or_404(TouristSpot, id=spot_id)
    return render(request, 'spot_detail.html', {'spot': spot})

@login_required
def delete_tourist_spot(request, spot_id):
    spot = get_object_or_404(TouristSpot, id=spot_id)
    
    # Check if user is authorized to delete (owner or superuser)
    if request.user != spot.created_by and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to delete this spot.")
    
    if request.method == 'POST':
        spot_name = spot.name
        spot.delete()
        messages.success(request, f'"{spot_name}" has been deleted successfully!')
        return redirect('home')
    return redirect('home')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TouristSpot
from .forms import TouristSpotForm

@login_required
def update_spot(request, spot_id):
    """Update tourist spot information"""
    # Check if user is admin
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to update spots.')
        return redirect('home')
    
    spot = get_object_or_404(TouristSpot, id=spot_id)
    
    if request.method == 'POST':
        form = TouristSpotForm(request.POST, request.FILES, instance=spot)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{spot.name}" updated successfully!')
            return redirect('home')
    else:
        form = TouristSpotForm(instance=spot)
    
    return render(request, 'update_spot.html', {
        'form': form,
        'spot': spot
    })

@login_required
def delete_spot(request, spot_id):
    """Delete tourist spot"""
    # Check if user is admin
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete spots.')
        return redirect('home')
    
    spot = get_object_or_404(TouristSpot, id=spot_id)
    
    if request.method == 'POST':
        spot_name = spot.name
        spot.delete()
        messages.success(request, f'"{spot_name}" deleted successfully!')
        return redirect('home')
    
    return render(request, 'delete_confirm.html', {'spot': spot})
def manage_spots(request):
    spots = TouristSpot.objects.all()
    return render(request, 'manage_spots.html', {'spots': spots})