from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import CustomLoginView, home, about, contact, travel_history, register, custom_logout
from accounts.views import study_tour_detail, book_study_tour, booking_confirmation, my_bookings, cancel_booking
from accounts.views import admin_booking_management, approve_booking, pending_booking, cancel_booking_admin
from accounts.views import restore_booking, delete_booking, approve_all_pending, restore_all_cancelled
from accounts.views import update_booking_status, get_available_slots
from accounts.views import add_spot, spot_detail, update_spot, delete_spot
from accounts.views import mark_message_read, mark_message_replied, delete_message
from accounts.views import select_package_category, category_packages, add_package, edit_package, delete_package
from accounts.views import book_package, my_package_bookings, cancel_package_booking
from accounts.views import get_booking_payment, submit_payment, admin_package_bookings
from accounts.views import approve_package_booking, reject_package_booking
from accounts.views import approve_trip_request, reject_trip_request, delete_trip_request
from accounts.views import verify_payment, reject_payment

urlpatterns = [
    # Basic pages
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('travel-history/', travel_history, name='travel_history'),
    
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='custom_logout'),
    
    # Booking URLs
    path('packages/', study_tour_detail, name='packages'),
    path('book-study-tour/', book_study_tour, name='book_study_tour'),
    path('booking-confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    
    # Tourist Spot URLs
    path('add-spot/', add_spot, name='add_spot'),
    path('spot/<int:spot_id>/', spot_detail, name='spot_detail'),
    path('spot/<int:spot_id>/update/', update_spot, name='update_spot'),
    path('spot/<int:spot_id>/delete/', delete_spot, name='delete_spot'),
    
    # Admin Booking URLs
    path('admin/bookings/', admin_booking_management, name='admin_booking_management'),
    path('admin/bookings/approve/<int:booking_id>/', approve_booking, name='approve_booking'),
    path('admin/bookings/pending/<int:booking_id>/', pending_booking, name='pending_booking'),
    path('admin/bookings/cancel/<int:booking_id>/', cancel_booking_admin, name='cancel_booking_admin'),
    path('admin/bookings/restore/<int:booking_id>/', restore_booking, name='restore_booking'),
    path('admin/bookings/delete/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('admin/bookings/approve-all-pending/', approve_all_pending, name='approve_all_pending'),
    path('admin/bookings/restore-all-cancelled/', restore_all_cancelled, name='restore_all_cancelled'),
    path('admin/bookings/update-status/<int:booking_id>/', update_booking_status, name='update_booking_status'),
    
    # Contact Message Management URLs
    path('message/read/<int:message_id>/', mark_message_read, name='mark_message_read'),
    path('message/replied/<int:message_id>/', mark_message_replied, name='mark_message_replied'),
    path('message/delete/<int:message_id>/', delete_message, name='delete_message'),
    
    # API URLs
    path('api/available-slots/<int:date_id>/', get_available_slots, name='get_available_slots'),
    
    # Tour Package URLs
    path('packages/category/', select_package_category, name='select_package_category'),
    path('packages/category/<str:category>/', category_packages, name='category_packages'),
    path('packages/add/', add_package, name='add_package'),
    path('packages/<int:package_id>/edit/', edit_package, name='edit_package'),
    path('packages/<int:package_id>/delete/', delete_package, name='delete_package'),
    path('packages/<int:package_id>/book/', book_package, name='book_package'),
    
    # User Package Bookings URLs
    path('my-package-bookings/', my_package_bookings, name='my_package_bookings'),
    path('my-package-bookings/<int:booking_id>/cancel/', cancel_package_booking, name='cancel_package_booking'),
    
    # Payment API URLs
    path('api/booking/<int:booking_id>/payment/', get_booking_payment, name='get_booking_payment'),
    path('api/booking/<int:booking_id>/submit-payment/', submit_payment, name='submit_payment'),
    
    # Admin Package Management URLs
    path('admin/package-bookings/', admin_package_bookings, name='admin_package_bookings'),
    path('admin/package-bookings/approve/<int:booking_id>/', approve_package_booking, name='approve_package_booking'),
    path('admin/package-bookings/reject/<int:booking_id>/', reject_package_booking, name='reject_package_booking'),
    
    # Custom Trip Request URLs
    path('admin/trip-requests/approve/<int:request_id>/', approve_trip_request, name='approve_trip_request'),
    path('admin/trip-requests/reject/<int:request_id>/', reject_trip_request, name='reject_trip_request'),
    path('admin/trip-requests/delete/<int:request_id>/', delete_trip_request, name='delete_trip_request'),
    
    # Payment Management URLs
    path('payment/verify/<int:payment_id>/', verify_payment, name='verify_payment'),
    path('payment/reject/<int:payment_id>/', reject_payment, name='reject_payment'),
    
    # Include Django admin
    path('admin/', admin.site.urls),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)