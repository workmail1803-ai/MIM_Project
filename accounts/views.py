from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.db import OperationalError
from .forms import CustomUserCreationForm, ContactMessageForm, CustomTripRequestForm
from .models import StudyTour, TourDate, TourInclusion, StudyTourBooking, ContactMessage, CustomTripRequest
from tourist_spots.models import TouristSpot, TourPackage, PackageBooking, Payment
from tourist_spots.forms import TouristSpotForm, TourPackageForm, PackageBookingForm

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
    """Home page view with tourist spots"""
    try:
        spots = TouristSpot.objects.all()
    except OperationalError:
        spots = []
        messages.warning(request, "Database is being set up. Please wait a moment and refresh.")
    return render(request, 'home.html', {'spots': spots})

def about(request):
    """About page view"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view - Admin sees messages, Students/Users can send messages and travel requests"""
    is_admin = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
    
    if is_admin:
        contact_messages = ContactMessage.objects.all()
        custom_requests = CustomTripRequest.objects.all()
        unread_count = contact_messages.filter(status='unread').count()
        pending_requests_count = custom_requests.filter(status='pending').count()
        
        return render(request, 'contact.html', {
            'contact_messages': contact_messages,
            'custom_requests': custom_requests,
            'unread_count': unread_count,
            'pending_requests_count': pending_requests_count,
            'is_admin_view': True
        })
    
    # Students/Users side
    contact_form = ContactMessageForm(prefix='contact')
    request_form = CustomTripRequestForm(prefix='request')
    
    if request.method == 'POST':
        if 'submit_contact' in request.POST:
            contact_form = ContactMessageForm(request.POST, prefix='contact')
            if contact_form.is_valid():
                msg = contact_form.save(commit=False)
                if request.user.is_authenticated:
                    msg.user = request.user
                msg.save()
                messages.success(request, '✅ Your message has been sent successfully!')
                return redirect('contact')
            else:
                messages.error(request, '❌ Please correct the errors in your contact message.')
        
        elif 'submit_request' in request.POST:
            request_form = CustomTripRequestForm(request.POST, prefix='request')
            if request_form.is_valid():
                trip_request = request_form.save(commit=False)
                if request.user.is_authenticated:
                    trip_request.user = request.user
                trip_request.save()
                messages.success(request, '✅ Your travel request has been submitted and will be reviewed by admin!')
                return redirect('contact')
            else:
                messages.error(request, '❌ Please correct the errors in your custom trip request.')
    
    else:
        # Pre-fill standard form if authenticated
        if request.user.is_authenticated:
            contact_form = ContactMessageForm(prefix='contact', initial={
                'first_name': request.user.first_name or request.user.username,
                'last_name': request.user.last_name or '',
                'email': request.user.email,
            })
            request_form = CustomTripRequestForm(prefix='request', initial={
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
                'phone': getattr(request.user, 'profile', None).phone if hasattr(request.user, 'profile') else ''
            })

    return render(request, 'contact.html', {
        'contact_form': contact_form,
        'request_form': request_form,
        'is_admin_view': False
    })

@staff_member_required
def approve_trip_request(request, request_id):
    """Admin approves a custom trip request"""
    trip_request = get_object_or_404(CustomTripRequest, id=request_id)
    trip_request.status = 'approved'
    trip_request.save()
    messages.success(request, f'✅ Trip request #{request_id} from {trip_request.full_name} has been approved.')
    return redirect('contact')

@staff_member_required
def reject_trip_request(request, request_id):
    """Admin rejects a custom trip request"""
    trip_request = get_object_or_404(CustomTripRequest, id=request_id)
    trip_request.status = 'rejected'
    trip_request.save()
    messages.warning(request, f'❌ Trip request #{request_id} from {trip_request.full_name} has been rejected.')
    return redirect('contact')

@staff_member_required
def delete_trip_request(request, request_id):
    """Admin deletes a custom trip request"""
    trip_request = get_object_or_404(CustomTripRequest, id=request_id)
    trip_request.delete()
    messages.success(request, f'🗑️ Trip request #{request_id} deleted.')
    return redirect('contact')

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
    # Allowing GET for easier deletion via link if forms are blocked
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
    """Packages page - shows admin-created TourPackages"""
    # Get all active TourPackages
    tour_packages = TourPackage.objects.filter(is_active=True)
    
    # For admins, show all packages including inactive ones
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        tour_packages = TourPackage.objects.all()
    
    context = {
        'tour_packages': tour_packages,
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

# Tourist Spot Views
@login_required
def add_spot(request):
    """Add a new tourist spot"""
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
    """View tourist spot details"""
    spot = get_object_or_404(TouristSpot, id=spot_id)
    return render(request, 'spot_detail.html', {'spot': spot})

@login_required
def update_spot(request, spot_id):
    """Update tourist spot information"""
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


# =====================================================
# Tour Package Views
# =====================================================

# Category information helper
CATEGORY_INFO = {
    'study_tour': {
        'name': 'Study Tour Packages',
        'icon': 'fa-graduation-cap',
        'description': 'Educational tours for students to explore and learn from different places'
    },
    'cycling': {
        'name': 'Cycling Packages',
        'icon': 'fa-bicycle',
        'description': 'Adventure cycling tours and marathon events for cycling enthusiasts'
    },
    'university_program': {
        'name': 'University Programs',
        'icon': 'fa-university',
        'description': 'Professional development programs and university events'
    }
}

@login_required
@user_passes_test(is_admin)
def select_package_category(request):
    """Admin selects category before adding package"""
    return render(request, 'select_package_category.html')


def category_packages(request, category):
    """List packages by category for users and admins"""
    # Validate category
    if category not in CATEGORY_INFO:
        messages.error(request, 'Invalid category.')
        return redirect('home')
    
    # Get category info
    cat_info = CATEGORY_INFO[category]
    
    # Get packages for this category
    tour_packages = TourPackage.objects.filter(category=category, is_active=True)
    
    # For admins, show all packages including inactive ones
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        tour_packages = TourPackage.objects.filter(category=category)
    
    context = {
        'tour_packages': tour_packages,
        'category_name': cat_info['name'],
        'category_icon': cat_info['icon'],
        'category_description': cat_info['description'],
        'category_slug': category,
    }
    
    return render(request, 'category_packages.html', context)


@login_required
@user_passes_test(is_admin)
def add_package(request):
    """Admin adds new tour package"""
    category = request.GET.get('category', 'study_tour')
    
    if category not in CATEGORY_INFO:
        category = 'study_tour'
    
    cat_info = CATEGORY_INFO[category]
    
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.created_by = request.user
            package.save()
            messages.success(request, f'Package "{package.name}" has been created successfully!')
            return redirect('category_packages', category=package.category)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TourPackageForm(initial={'category': category})
    
    context = {
        'form': form,
        'category_name': cat_info['name'],
        'category_icon': cat_info['icon'],
        'category_slug': category,
    }
    
    return render(request, 'add_package.html', context)


@login_required
@user_passes_test(is_admin)
def edit_package(request, package_id):
    """Admin edits tour package"""
    package = get_object_or_404(TourPackage, id=package_id)
    
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, f'Package "{package.name}" has been updated successfully!')
            return redirect('category_packages', category=package.category)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TourPackageForm(instance=package)
    
    context = {
        'form': form,
        'package': package,
    }
    
    return render(request, 'edit_package.html', context)


@login_required
@user_passes_test(is_admin)
def delete_package(request, package_id):
    """Admin deletes tour package"""
    package = get_object_or_404(TourPackage, id=package_id)
    category = package.category
    
    if request.method == 'POST':
        package_name = package.name
        package.delete()
        messages.success(request, f'Package "{package_name}" has been deleted.')
        return redirect('category_packages', category=category)
    
    return render(request, 'delete_package.html', {'package': package})


@login_required
def book_package(request, package_id):
    """User books a tour package"""
    package = get_object_or_404(TourPackage, id=package_id, is_active=True)
    
    # Admins shouldn't book packages
    if request.user.is_staff or request.user.is_superuser:
        messages.warning(request, 'Administrators cannot book packages. Please use a student account.')
        return redirect('category_packages', category=package.category)
    
    if request.method == 'POST':
        form = PackageBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.save()
            messages.success(request, f'Your booking for "{package.name}" has been submitted! You will be notified once it\'s approved.')
            return redirect('my_package_bookings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill form with user info if available
        initial_data = {
            'student_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        form = PackageBookingForm(initial=initial_data)
    
    context = {
        'form': form,
        'package': package,
    }
    
    return render(request, 'book_package.html', context)


@login_required
def my_package_bookings(request):
    """User views their package bookings"""
    bookings = PackageBooking.objects.filter(user=request.user).select_related('package')
    
    # Mark bookings as notified when student views them
    unnotified = bookings.filter(student_notified=False, status__in=['approved', 'rejected'])
    for booking in unnotified:
        booking.student_notified = True
        booking.save()
    
    return render(request, 'my_package_bookings.html', {'bookings': bookings})


@login_required
def cancel_package_booking(request, booking_id):
    """User cancels their pending package booking"""
    booking = get_object_or_404(PackageBooking, id=booking_id, user=request.user)
    
    if booking.status != 'pending':
        messages.error(request, 'You can only cancel pending bookings.')
        return redirect('my_package_bookings')
    
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Your booking has been cancelled.')
    return redirect('my_package_bookings')


@login_required
def get_booking_payment(request, booking_id):
    """API: Get payment info for a booking"""
    booking = get_object_or_404(PackageBooking, id=booking_id)
    
    # Check authorization - user can only see their own bookings, admin can see all
    if not (request.user == booking.user or request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    # Get the latest payment
    payment = booking.payments.first()
    
    if payment:
        total_price = float(booking.package.price * booking.num_persons)
        amount_paid = float(payment.amount_paid)
        return JsonResponse({
            'has_payment': True,
            'amount_paid': amount_paid,
            'total_price': total_price,
            'remaining_amount': total_price - amount_paid,
            'status': payment.status,
            'bkash_last_4': payment.bkash_last_4,
        })
    else:
        total_price = float(booking.package.price * booking.num_persons)
        return JsonResponse({
            'has_payment': False,
            'total_price': total_price,
        })


@login_required
def submit_payment(request, booking_id):
    """API: Submit a payment for a booking"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    booking = get_object_or_404(PackageBooking, id=booking_id, user=request.user)
    
    if booking.status != 'approved':
        return JsonResponse({'error': 'Booking must be approved to submit payment'}, status=400)
    
    amount_paid = request.POST.get('amount_paid')
    bkash_last_4 = request.POST.get('bkash_last_4')
    
    errors = {}
    
    if not amount_paid:
        errors['amount_paid'] = ['Amount is required']
    else:
        try:
            amount_paid = float(amount_paid)
            if amount_paid <= 0:
                errors['amount_paid'] = ['Amount must be greater than 0']
        except ValueError:
            errors['amount_paid'] = ['Invalid amount']
    
    if not bkash_last_4:
        errors['bkash_last_4'] = ['bKash last 4 digits are required']
    elif len(bkash_last_4) != 4 or not bkash_last_4.isdigit():
        errors['bkash_last_4'] = ['Please enter exactly 4 digits']
    
    if errors:
        return JsonResponse({'success': False, 'details': errors})
    
    # Create or update payment
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'amount_paid': amount_paid,
            'bkash_last_4': bkash_last_4,
            'status': 'pending'
        }
    )
    
    if not created:
        payment.amount_paid = amount_paid
        payment.bkash_last_4 = bkash_last_4
        payment.status = 'pending'
        payment.save()
    
    return JsonResponse({'success': True})


@login_required
@user_passes_test(is_admin)
def admin_package_bookings(request):
    """Admin view to manage all package bookings"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    bookings = PackageBooking.objects.all().select_related('user', 'package').order_by('-created_at')
    
    if search_query:
        bookings = bookings.filter(
            Q(student_name__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(package__name__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Statistics
    total_bookings = bookings.count()
    pending_count = bookings.filter(status='pending').count()
    approved_count = bookings.filter(status='approved').count()
    rejected_count = bookings.filter(status='rejected').count()
    
    # Pagination
    paginator = Paginator(bookings, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'bookings': page_obj,
        'total_bookings': total_bookings,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin_package_bookings.html', context)


@login_required
@user_passes_test(is_admin)
def approve_package_booking(request, booking_id):
    """Admin approves a package booking"""
    if request.method == 'POST':
        booking = get_object_or_404(PackageBooking, id=booking_id)
        booking.status = 'approved'
        booking.student_notified = False  # Reset so student gets notification
        admin_notes = request.POST.get('admin_notes', '')
        if admin_notes:
            booking.admin_notes = admin_notes
        booking.save()
        messages.success(request, f'Booking #{booking_id} has been approved.')
    return redirect('admin_package_bookings')


@login_required
@user_passes_test(is_admin)
def reject_package_booking(request, booking_id):
    """Admin rejects a package booking"""
    if request.method == 'POST':
        booking = get_object_or_404(PackageBooking, id=booking_id)
        booking.status = 'rejected'
        booking.student_notified = False  # Reset so student gets notification
        admin_notes = request.POST.get('admin_notes', '')
        if admin_notes:
            booking.admin_notes = admin_notes
        booking.save()
        messages.success(request, f'Booking #{booking_id} has been rejected.')
    return redirect('admin_package_bookings')


@login_required
@user_passes_test(is_admin)
def verify_payment(request, payment_id):
    """Admin verifies a student payment"""
    if request.method == 'POST':
        payment = get_object_or_404(Payment, id=payment_id)
        payment.status = 'verified'
        payment.save()
        messages.success(request, f'Payment from {payment.booking.student_name} has been verified.')
    return redirect('admin_package_bookings')


@login_required
@user_passes_test(is_admin)
def reject_payment(request, payment_id):
    """Admin rejects a student payment"""
    if request.method == 'POST':
        payment = get_object_or_404(Payment, id=payment_id)
        payment.status = 'rejected'
        admin_notes = request.POST.get('admin_notes', '')
        if admin_notes:
            payment.admin_notes = admin_notes
        payment.save()
        messages.success(request, f'Payment from {payment.booking.student_name} has been rejected.')
    return redirect('admin_package_bookings')

