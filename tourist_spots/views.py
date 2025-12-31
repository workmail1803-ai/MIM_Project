from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import OperationalError
from django.contrib.auth.forms import UserCreationForm
from .models import TouristSpot, TourPackage, PackageBooking, Payment
from .forms import TouristSpotForm, TourPackageForm, PackageBookingForm, PaymentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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

def travel_history(request):
    return render(request, 'travel_history.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    """Contact page view - Admin sees messages, Students/Users can send messages"""
    from accounts.models import ContactMessage
    from accounts.forms import ContactMessageForm
    
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


# Tour Package Views
from .models import TourPackage, PackageBooking
from .forms import TourPackageForm, PackageBookingForm

def packages(request):
    """Display all tour packages organized by category with horizontal scrolling"""
    study_tour_packages = TourPackage.objects.filter(is_active=True, category='study_tour')
    cycling_packages = TourPackage.objects.filter(is_active=True, category='cycling')
    university_packages = TourPackage.objects.filter(is_active=True, category='university_program')
    
    return render(request, 'packages.html', {
        'study_tour_packages': study_tour_packages,
        'cycling_packages': cycling_packages,
        'university_packages': university_packages,
    })


def study_tour_packages(request):
    """Display Study Tour packages - Login required for students"""
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view Study Tour packages.')
        return redirect('login')
    
    tour_packages = TourPackage.objects.filter(is_active=True, category='study_tour')
    return render(request, 'category_packages.html', {
        'tour_packages': tour_packages,
        'category_name': 'Study Tour Packages',
        'category_slug': 'study_tour',
        'category_icon': 'fa-graduation-cap',
        'category_description': '"We don\'t just travel to see places; we travel to understand them."'
    })


def cycling_packages(request):
    """Display Cycling packages - Login required for students"""
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view Cycling packages.')
        return redirect('login')
    
    tour_packages = TourPackage.objects.filter(is_active=True, category='cycling')
    return render(request, 'category_packages.html', {
        'tour_packages': tour_packages,
        'category_name': 'Cycling Packages',
        'category_slug': 'cycling',
        'category_icon': 'fa-bicycle',
        'category_description': '"Life is like riding a bicycle — to keep your balance, you must keep moving."'
    })


def university_program_packages(request):
    """Display University Program packages - Login required for students"""
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view University Program packages.')
        return redirect('login')
    
    tour_packages = TourPackage.objects.filter(is_active=True, category='university_program')
    return render(request, 'category_packages.html', {
        'tour_packages': tour_packages,
        'category_name': 'University Programs',
        'category_slug': 'university_program',
        'category_icon': 'fa-university',
        'category_description': '"Programs build skills, but more importantly, they build people."'
    })


@login_required
def select_package_category(request):
    """Select category before adding a package - Admin only"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to add packages.')
        return redirect('home')
    
    return render(request, 'select_package_category.html')


@login_required
def add_package(request):
    """Add a new tour package - Admin only"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to add packages.')
        return redirect('packages')
    
    # Get category from query parameter - redirect to selection if not provided
    category = request.GET.get('category')
    if not category and request.method != 'POST':
        return redirect('select_package_category')
    
    # Get category from query parameter
    initial_category = request.GET.get('category', 'study_tour')
    
    # Category display names
    category_names = {
        'study_tour': 'Study Tour Package',
        'cycling': 'Cycling Package',
        'university_program': 'University Program'
    }
    category_icons = {
        'study_tour': 'fa-graduation-cap',
        'cycling': 'fa-bicycle',
        'university_program': 'fa-university'
    }
    
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.created_by = request.user
            package.save()
            messages.success(request, f'Package "{package.name}" has been added successfully!')
            
            # Redirect to the appropriate category page
            category = package.category
            if category == 'study_tour':
                return redirect('study_tour_packages')
            elif category == 'cycling':
                return redirect('cycling_packages')
            elif category == 'university_program':
                return redirect('university_program_packages')
            return redirect('packages')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TourPackageForm(initial={'category': initial_category})
    
    return render(request, 'add_package.html', {
        'form': form,
        'category_name': category_names.get(initial_category, 'Package'),
        'category_icon': category_icons.get(initial_category, 'fa-box'),
        'category_slug': initial_category
    })

@login_required
def edit_package(request, package_id):
    """Edit a tour package - Admin only"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to edit packages.')
        return redirect('packages')
    
    package = get_object_or_404(TourPackage, id=package_id)
    
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, f'Package "{package.name}" updated successfully!')
            return redirect('packages')
    else:
        form = TourPackageForm(instance=package)
    
    return render(request, 'edit_package.html', {'form': form, 'package': package})

@login_required
def delete_package(request, package_id):
    """Delete a tour package - Admin only"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete packages.')
        return redirect('packages')
    
    package = get_object_or_404(TourPackage, id=package_id)
    
    if request.method == 'POST':
        package_name = package.name
        package.delete()
        messages.success(request, f'Package "{package_name}" deleted successfully!')
        return redirect('packages')
    
    return render(request, 'delete_package.html', {'package': package})


@login_required
def book_package(request, package_id):
    """Book a tour package - Student booking form (Admin cannot book)"""
    # Prevent admin from booking
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, 'Administrators cannot book packages. Only students can book.')
        return redirect('packages')
    
    package = get_object_or_404(TourPackage, id=package_id, is_active=True)
    
    if request.method == 'POST':
        form = PackageBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.package = package
            booking.user = request.user
            booking.save()
            messages.success(request, f'Your booking request for "{package.name}" has been submitted! Please wait for admin approval.')
            return redirect('my_package_bookings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill email if user has one
        initial_data = {}
        if request.user.email:
            initial_data['email'] = request.user.email
        form = PackageBookingForm(initial=initial_data)
    
    return render(request, 'book_package.html', {'form': form, 'package': package})


@login_required
def my_package_bookings(request):
    """View user's package bookings and mark notifications as read"""
    bookings = PackageBooking.objects.filter(user=request.user)
    
    # Mark unread notifications as read when student views the page
    unread_bookings = bookings.filter(
        status__in=['approved', 'rejected'],
        student_notified=False
    )
    unread_bookings.update(student_notified=True)
    
    return render(request, 'my_package_bookings.html', {'bookings': bookings})


@login_required
def cancel_package_booking(request, booking_id):
    """Cancel a package booking"""
    booking = get_object_or_404(PackageBooking, id=booking_id, user=request.user)
    
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'Only pending bookings can be cancelled.')
    
    return redirect('my_package_bookings')


# Admin Package Booking Management
@login_required
def admin_package_bookings(request):
    """Admin view to manage all package bookings"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('packages')
    
    status_filter = request.GET.get('status', 'all')
    
    if status_filter == 'all':
        bookings = PackageBooking.objects.all()
    else:
        bookings = PackageBooking.objects.filter(status=status_filter)
    
    pending_count = PackageBooking.objects.filter(status='pending').count()
    approved_count = PackageBooking.objects.filter(status='approved').count()
    rejected_count = PackageBooking.objects.filter(status='rejected').count()
    
    return render(request, 'admin_package_bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    })


@login_required
def approve_package_booking(request, booking_id):
    """Approve a package booking"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('packages')
    
    booking = get_object_or_404(PackageBooking, id=booking_id)
    booking.status = 'approved'
    booking.save()
    messages.success(request, f'Booking for {booking.student_name} has been approved!')
    return redirect('admin_package_bookings')


@login_required
def reject_package_booking(request, booking_id):
    """Reject a package booking"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('packages')
    
    booking = get_object_or_404(PackageBooking, id=booking_id)
    booking.status = 'rejected'
    if request.method == 'POST':
        booking.admin_notes = request.POST.get('admin_notes', '')
    booking.save()
    messages.success(request, f'Booking for {booking.student_name} has been rejected.')
    return redirect('admin_package_bookings')


# Payment Views
@login_required
@require_POST
def submit_payment(request, booking_id):
    """Submit payment for a booking - Creates or updates Payment record"""
    booking = get_object_or_404(PackageBooking, id=booking_id, user=request.user)
    
    # Only approved bookings can receive payment
    if booking.status != 'approved':
        return JsonResponse({'error': 'Booking must be approved before payment.'}, status=400)
    
    form = PaymentForm(request.POST)
    if form.is_valid():
        # Check if payment already exists for this booking
        payment = Payment.objects.filter(booking=booking).first()
        
        if payment:
            # Update existing payment
            payment.amount_paid = form.cleaned_data['amount_paid']
            payment.bkash_last_4 = form.cleaned_data['bkash_last_4']
            payment.status = 'pending'  # Reset to pending for re-verification
            payment.save()
        else:
            # Create new payment
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()
        
        return JsonResponse({'success': True, 'message': 'Payment submitted successfully. Admin will verify it shortly.'})
    else:
        errors = form.errors.as_json()
        return JsonResponse({'error': 'Invalid payment information', 'details': form.errors}, status=400)


@login_required
def verify_payment(request, payment_id):
    """Admin verifies a payment - Mark as verified"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('admin_package_bookings')
    
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        admin_notes = request.POST.get('admin_notes', '')
        payment.status = 'verified'
        payment.admin_notes = admin_notes
        payment.save()
        messages.success(request, f'Payment verified for {payment.booking.student_name}')
    
    return redirect('admin_package_bookings')


@login_required
def reject_payment(request, payment_id):
    """Admin rejects a payment"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('admin_package_bookings')
    
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        admin_notes = request.POST.get('admin_notes', '')
        payment.status = 'rejected'
        payment.admin_notes = admin_notes
        payment.save()
        messages.success(request, f'Payment rejected for {payment.booking.student_name}')
    
    return redirect('admin_package_bookings')


@login_required
def get_booking_payment(request, booking_id):
    """Get payment details for a booking - AJAX endpoint"""
    booking = get_object_or_404(PackageBooking, id=booking_id, user=request.user)
    
    payment = Payment.objects.filter(booking=booking).first()
    
    if payment:
        data = {
            'has_payment': True,
            'amount_paid': float(payment.amount_paid),
            'bkash_last_4': payment.bkash_last_4,
            'status': payment.status,
            'total_price': float(booking.package.price),
            'remaining_amount': float(booking.package.price - payment.amount_paid),
        }
    else:
        data = {
            'has_payment': False,
            'total_price': float(booking.package.price),
        }
    
    return JsonResponse(data)


# Contact Message Management Views
@login_required
def mark_message_read(request, message_id):
    """Mark a contact message as read"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('contact')
    
    from accounts.models import ContactMessage
    message = get_object_or_404(ContactMessage, id=message_id)
    message.status = 'read'
    message.save()
    messages.success(request, 'Message marked as read.')
    return redirect('contact')


@login_required
def mark_message_replied(request, message_id):
    """Mark a contact message as replied"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('contact')
    
    from accounts.models import ContactMessage
    message = get_object_or_404(ContactMessage, id=message_id)
    message.status = 'replied'
    message.save()
    messages.success(request, 'Message marked as replied.')
    return redirect('contact')


@login_required
def delete_contact_message(request, message_id):
    """Delete a contact message"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('contact')
    
    from accounts.models import ContactMessage
    message = get_object_or_404(ContactMessage, id=message_id)
    message.delete()
    messages.success(request, 'Message deleted successfully.')
    return redirect('contact')


# ============== Travel Request Views ==============

@login_required
def submit_travel_request(request):
    """Student submits a travel place request"""
    from .forms import TravelRequestForm
    from .models import TravelRequest
    
    if request.method == 'POST':
        form = TravelRequestForm(request.POST)
        if form.is_valid():
            travel_request = form.save(commit=False)
            travel_request.user = request.user
            travel_request.save()
            messages.success(request, '✅ Your travel request has been submitted successfully! An admin will review it soon.')
            return redirect('my_travel_requests')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = TravelRequestForm()
    
    return render(request, 'travel_request_form.html', {'form': form})


@login_required
def my_travel_requests(request):
    """View student's own travel requests"""
    from .models import TravelRequest
    
    requests = TravelRequest.objects.filter(user=request.user).order_by('-created_at')
    
    # Count statistics
    pending_count = requests.filter(status='pending').count()
    approved_count = requests.filter(status='approved').count()
    rejected_count = requests.filter(status='rejected').count()
    
    return render(request, 'my_travel_requests.html', {
        'travel_requests': requests,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    })


@login_required
def admin_travel_requests(request):
    """Admin view to manage all travel requests"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied. Admin access required.')
        return redirect('home')
    
    from .models import TravelRequest
    
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    requests = TravelRequest.objects.all().select_related('user').order_by('-created_at')
    
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    if search_query:
        requests = requests.filter(
            models.Q(place_name__icontains=search_query) |
            models.Q(location__icontains=search_query) |
            models.Q(user__username__icontains=search_query) |
            models.Q(user__first_name__icontains=search_query)
        )
    
    # Count statistics
    total_count = TravelRequest.objects.count()
    pending_count = TravelRequest.objects.filter(status='pending').count()
    approved_count = TravelRequest.objects.filter(status='approved').count()
    rejected_count = TravelRequest.objects.filter(status='rejected').count()
    
    return render(request, 'admin_travel_requests.html', {
        'travel_requests': requests,
        'total_count': total_count,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'status_filter': status_filter,
        'search_query': search_query,
    })


@login_required
def approve_travel_request(request, request_id):
    """Admin approves a travel request"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('home')
    
    from .models import TravelRequest
    
    travel_request = get_object_or_404(TravelRequest, id=request_id)
    
    if request.method == 'POST':
        admin_response = request.POST.get('admin_response', '')
        travel_request.status = 'approved'
        travel_request.admin_response = admin_response
        travel_request.save()
        messages.success(request, f'✅ Travel request for "{travel_request.place_name}" has been approved!')
    
    return redirect('admin_travel_requests')


@login_required
def reject_travel_request(request, request_id):
    """Admin rejects a travel request"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('home')
    
    from .models import TravelRequest
    
    travel_request = get_object_or_404(TravelRequest, id=request_id)
    
    if request.method == 'POST':
        admin_response = request.POST.get('admin_response', '')
        travel_request.status = 'rejected'
        travel_request.admin_response = admin_response
        travel_request.save()
        messages.success(request, f'❌ Travel request for "{travel_request.place_name}" has been rejected.')
    
    return redirect('admin_travel_requests')


@login_required
def delete_travel_request(request, request_id):
    """Delete a travel request (admin or owner)"""
    from .models import TravelRequest
    
    travel_request = get_object_or_404(TravelRequest, id=request_id)
    
    # Check permission - admin or owner can delete
    if not (request.user.is_staff or request.user.is_superuser or request.user == travel_request.user):
        messages.error(request, 'Permission denied.')
        return redirect('home')
    
    if request.method == 'POST':
        place_name = travel_request.place_name
        travel_request.delete()
        messages.success(request, f'Travel request for "{place_name}" has been deleted.')
    
    # Redirect based on user type
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_travel_requests')
    return redirect('my_travel_requests')