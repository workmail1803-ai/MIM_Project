from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .forms import CustomUserCreationForm, ContactMessageForm
from .models import StudyTour, TourDate, TourInclusion, StudyTourBooking, ContactMessage

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Login successful!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Login failed. Please check your credentials.')
        return super().form_invalid(form)

# Authentication Views
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            role = form.cleaned_data.get('role')
            if role == 'student':
                messages.success(request, 'Student registration successful! You can now access student features.')
            else:
                messages.success(request, 'Admin registration successful! You can now access admin features.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Basic Page Views
def home(request):
    """Home page view"""
    return render(request, 'home.html')

def about(request):
    """About page view"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view - Admin sees messages, Students/Users can send messages"""
    # Admin users see the message inbox
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        contact_messages = ContactMessage.objects.all()
        unread_count = contact_messages.filter(status='unread').count()
        return render(request, 'contact.html', {
            'contact_messages': contact_messages,
            'unread_count': unread_count,
            'is_admin_view': True
        })
    
    # Students/Users see the contact form
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.user = request.user
            message.save()
            messages.success(request, '✅ Your message has been sent successfully! We will get back to you within 24 hours.')
            return redirect('contact')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        # Pre-fill form for logged-in users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name or request.user.username,
                'last_name': request.user.last_name or '',
                'email': request.user.email,
            }
        form = ContactMessageForm(initial=initial_data)
    
    return render(request, 'contact.html', {
        'form': form,
        'is_admin_view': False
    })

@staff_member_required
def mark_message_read(request, message_id):
    """Mark a contact message as read"""
    message = get_object_or_404(ContactMessage, id=message_id)
    message.status = 'read'
    message.save()
    messages.success(request, 'Message marked as read.')
    return redirect('contact')

@staff_member_required
def mark_message_replied(request, message_id):
    """Mark a contact message as replied"""
    message = get_object_or_404(ContactMessage, id=message_id)
    message.status = 'replied'
    message.save()
    messages.success(request, 'Message marked as replied.')
    return redirect('contact')

@staff_member_required
def delete_message(request, message_id):
    """Delete a contact message"""
    message = get_object_or_404(ContactMessage, id=message_id)
    message.delete()
    messages.success(request, 'Message deleted successfully.')
    return redirect('contact')

def tourist_spots(request):
    """Tourist spots page view"""
    return render(request, 'tourist_spots.html')

@login_required
def travel_history(request):
    """Travel history page view with user's bookings"""
    bookings = StudyTourBooking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Calculate some statistics for the template
    total_trips = bookings.count()
    total_spent = bookings.aggregate(total=Sum('total_price'))['total'] or 0
    
    context = {
        'bookings': bookings,
        'total_trips': total_trips,
        'total_spent': total_spent,
    }
    
    return render(request, 'travel_history.html', context)

# Study Tour and Booking Views
def study_tour_detail(request, tour_id=None):
    """Study tour package details page"""
    try:
        if tour_id:
            study_tour = get_object_or_404(StudyTour, id=tour_id, is_active=True)
        else:
            study_tour = StudyTour.objects.filter(is_active=True).first()
        
        if not study_tour:
            return render(request, 'packages.html', {
                'study_tour': None,
                'tour_dates': [],
                'inclusions': [],
                'database_error': True
            })
        
        tour_dates = study_tour.dates.filter(is_available=True)
        inclusions = study_tour.inclusions.all()
        
        context = {
            'study_tour': study_tour,
            'tour_dates': tour_dates,
            'inclusions': inclusions,
            'database_error': False
        }
        
    except Exception as e:
        print(f"Error: {e}")
        context = {
            'study_tour': None,
            'tour_dates': [],
            'inclusions': [],
            'database_error': True
        }
    
    return render(request, 'packages.html', context)

@login_required
def book_study_tour(request):
    """Handle study tour booking"""
    if request.method == 'POST':
        try:
            study_tour_id = request.POST.get('study_tour')
            tour_date_id = request.POST.get('tour_date')
            special_requirements = request.POST.get('special_requirements', '')
            
            if not study_tour_id or not tour_date_id:
                messages.error(request, 'Please select a tour date.')
                return redirect('packages')
            
            study_tour = StudyTour.objects.get(id=study_tour_id)
            tour_date = TourDate.objects.get(id=tour_date_id)
            
            if tour_date.available_slots <= 0:
                messages.error(request, 'Sorry, no slots available for this date.')
                return redirect('packages')
            
            if StudyTourBooking.objects.filter(user=request.user, tour_date=tour_date).exists():
                messages.warning(request, 'You have already booked this tour date.')
                return redirect('packages')
            
            booking = StudyTourBooking.objects.create(
                user=request.user,
                study_tour=study_tour,
                tour_date=tour_date,
                total_price=study_tour.discounted_price,
                special_requirements=special_requirements,
                status='pending'
            )
            
            tour_date.available_slots -= 1
            tour_date.save()
            
            messages.success(request, '🎉 Study tour booked successfully! Our coordinator will contact you soon.')
            return redirect('booking_confirmation', booking_id=booking.id)
            
        except Exception as e:
            print(f"Booking error: {e}")
            messages.error(request, f'Sorry, there was an error: {str(e)}')
    
    return redirect('packages')

@login_required
def booking_confirmation(request, booking_id):
    """Booking confirmation page"""
    booking = get_object_or_404(StudyTourBooking, id=booking_id, user=request.user)
    return render(request, 'booking_confirmation.html', {'booking': booking})

@login_required
def my_bookings(request):
    """View to show all bookings for the current user"""
    bookings = StudyTourBooking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking and restore slots (user view)"""
    booking = get_object_or_404(StudyTourBooking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        # Restore the slot
        booking.tour_date.available_slots += 1
        booking.tour_date.save()
        
        # Update booking status
        booking.status = 'cancelled'
        booking.save()
        
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('my_bookings')
    
    return render(request, 'cancel_booking.html', {'booking': booking})

# API Views
def get_available_slots(request, date_id):
    """API endpoint to get available slots for a tour date"""
    tour_date = get_object_or_404(TourDate, id=date_id)
    return JsonResponse({'available_slots': tour_date.available_slots})

# Admin Views
def is_admin(user):
    """Check if user is admin"""
    return user.is_staff or user.is_superuser or getattr(user, 'role', None) == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_booking_management(request):
    """Admin view to manage all bookings"""
    # Get filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Start with all bookings
    bookings = StudyTourBooking.objects.all().select_related('user', 'study_tour', 'tour_date').order_by('-booking_date')
    
    # Apply filters
    if search_query:
        bookings = bookings.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(study_tour__name__icontains=search_query)
        )
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Get counts for statistics
    total_bookings = bookings.count()
    pending_count = bookings.filter(status='pending').count()
    confirmed_count = bookings.filter(status='confirmed').count()
    cancelled_count = bookings.filter(status='cancelled').count()
    completed_count = bookings.filter(status='completed').count()
    
    # Calculate total revenue from confirmed bookings
    total_revenue = bookings.filter(status='confirmed').aggregate(total=Sum('total_price'))['total'] or 0
    
    # Pagination
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'bookings': page_obj,
        'total_bookings': total_bookings,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'cancelled_count': cancelled_count,
        'completed_count': completed_count,
        'total_revenue': total_revenue,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin_booking_management.html', context)

@login_required
@user_passes_test(is_admin)
def approve_booking(request, booking_id):
    """Approve a specific booking"""
    if request.method == 'POST':
        try:
            booking = StudyTourBooking.objects.get(id=booking_id)
            booking.status = 'confirmed'
            booking.save()
            messages.success(request, f'Booking #{booking_id} has been approved.')
        except StudyTourBooking.DoesNotExist:
            messages.error(request, f'Booking #{booking_id} not found.')
    
    return redirect('admin_booking_management')

@login_required
@user_passes_test(is_admin)
def pending_booking(request, booking_id):
    """Set booking back to pending status"""
    if request.method == 'POST':
        try:
            booking = StudyTourBooking.objects.get(id=booking_id)
            booking.status = 'pending'
            booking.save()
            
            # Restore the slot
            booking.tour_date.available_slots += 1
            booking.tour_date.save()
            
            messages.success(request, f'Booking #{booking_id} has been set to pending.')
        except StudyTourBooking.DoesNotExist:
            messages.error(request, f'Booking #{booking_id} not found.')
    
    return redirect('admin_booking_management')

@login_required
@user_passes_test(is_admin)
def cancel_booking_admin(request, booking_id):
    """Cancel a booking (admin only)"""
    if request.method == 'POST':
        try:
            booking = StudyTourBooking.objects.get(id=booking_id)
            booking.status = 'cancelled'
            booking.save()
            
            # Restore the slot
            booking.tour_date.available_slots += 1
            booking.tour_date.save()
            
            messages.success(request, f'Booking #{booking_id} has been cancelled.')
        except StudyTourBooking.DoesNotExist:
            messages.error(request, f'Booking #{booking_id} not found.')
    
    return redirect('admin_booking_management')

@login_required
@user_passes_test(is_admin)
def restore_booking(request, booking_id):
    """Restore a cancelled booking"""
    if request.method == 'POST':
        try:
            booking = StudyTourBooking.objects.get(id=booking_id)
            booking.status = 'pending'
            booking.save()
            
            # Use a slot
            if booking.tour_date.available_slots > 0:
                booking.tour_date.available_slots -= 1
                booking.tour_date.save()
            
            messages.success(request, f'Booking #{booking_id} has been restored to pending status.')
        except StudyTourBooking.DoesNotExist:
            messages.error(request, f'Booking #{booking_id} not found.')
    
    return redirect('admin_booking_management')

@login_required
@user_passes_test(is_admin)
def delete_booking(request, booking_id):
    """Permanently delete a booking"""
    if request.method == 'POST':
        try:
            booking = StudyTourBooking.objects.get(id=booking_id)
            booking.delete()
            messages.success(request, f'Booking #{booking_id} has been permanently deleted.')
        except StudyTourBooking.DoesNotExist:
            messages.error(request, f'Booking #{booking_id} not found.')
    
    return redirect('admin_booking_management')

@login_required
@user_passes_test(is_admin)
def approve_all_pending(request):
    """Approve all pending bookings"""
    if request.method == 'POST':
        pending_bookings = StudyTourBooking.objects.filter(status='pending')
        count = pending_bookings.count()
        
        for booking in pending_bookings:
            booking.status = 'confirmed'
            booking.save()
        
        messages.success(request, f'All {count} pending bookings have been approved.')
    
    return redirect('admin_booking_management')

@login_required
@user_passes_test(is_admin)
def restore_all_cancelled(request):
    """Restore all cancelled bookings"""
    if request.method == 'POST':
        cancelled_bookings = StudyTourBooking.objects.filter(status='cancelled')
        count = cancelled_bookings.count()
        
        for booking in cancelled_bookings:
            booking.status = 'pending'
            booking.save()
            
            # Use a slot
            if booking.tour_date.available_slots > 0:
                booking.tour_date.available_slots -= 1
                booking.tour_date.save()
        
        messages.success(request, f'All {count} cancelled bookings have been restored to pending status.')
    
    return redirect('admin_booking_management')

@login_required
@user_passes_test(is_admin)
def update_booking_status(request, booking_id):
    """Update booking status dynamically"""
    if request.method == 'POST':
        try:
            booking = StudyTourBooking.objects.get(id=booking_id)
            new_status = request.POST.get('status')
            
            if new_status in dict(StudyTourBooking.STATUS_CHOICES):
                # Handle slot management based on status change
                old_status = booking.status
                
                if old_status in ['confirmed', 'pending'] and new_status == 'cancelled':
                    # Restore slot when cancelling
                    booking.tour_date.available_slots += 1
                    booking.tour_date.save()
                elif old_status == 'cancelled' and new_status in ['confirmed', 'pending']:
                    # Use slot when restoring from cancelled
                    if booking.tour_date.available_slots > 0:
                        booking.tour_date.available_slots -= 1
                        booking.tour_date.save()
                
                booking.status = new_status
                booking.save()
                messages.success(request, f'Booking #{booking_id} status updated to {new_status}.')
            else:
                messages.error(request, 'Invalid status.')
                
        except StudyTourBooking.DoesNotExist:
            messages.error(request, f'Booking #{booking_id} not found.')
    
    return redirect('admin_booking_management')
@login_required
@user_passes_test(is_admin)
def restore_booking(request, booking_id):
    """Restore a cancelled booking"""
    if request.method == 'POST':
        try:
            booking = StudyTourBooking.objects.get(id=booking_id)
            booking.status = 'pending'
            booking.save()
            
            # Use a slot
            if booking.tour_date.available_slots > 0:
                booking.tour_date.available_slots -= 1
                booking.tour_date.save()
            
            messages.success(request, f'Booking #{booking_id} has been restored to pending status.')
        except StudyTourBooking.DoesNotExist:
            messages.error(request, f'Booking #{booking_id} not found.')
    
    return redirect('admin_booking_management')