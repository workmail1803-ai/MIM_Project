from django.urls import path, include
from django.contrib import admin
from accounts.views import CustomLoginView, home, about, contact, travel_history, register, custom_logout
from accounts.views import study_tour_detail, book_study_tour, booking_confirmation, my_bookings, cancel_booking
from accounts.views import admin_booking_management, approve_booking, pending_booking, cancel_booking_admin
from accounts.views import restore_booking, delete_booking, approve_all_pending, restore_all_cancelled
from accounts.views import update_booking_status, get_available_slots, tourist_spots

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
    
    # Admin URLs
    path('admin/bookings/', admin_booking_management, name='admin_booking_management'),
    path('admin/bookings/approve/<int:booking_id>/', approve_booking, name='approve_booking'),
    path('admin/bookings/pending/<int:booking_id>/', pending_booking, name='pending_booking'),
    path('admin/bookings/cancel/<int:booking_id>/', cancel_booking_admin, name='cancel_booking_admin'),
    path('admin/bookings/restore/<int:booking_id>/', restore_booking, name='restore_booking'),
    path('admin/bookings/delete/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('admin/bookings/approve-all-pending/', approve_all_pending, name='approve_all_pending'),
    path('admin/bookings/restore-all-cancelled/', restore_all_cancelled, name='restore_all_cancelled'),
    path('admin/bookings/update-status/<int:booking_id>/', update_booking_status, name='update_booking_status'),
    
    # API URLs
    path('api/available-slots/<int:date_id>/', get_available_slots, name='get_available_slots'),
    
    # Include Django admin
    path('admin/', admin.site.urls),
    
    # Include tourist spots
    path('tourist-spots/', include('tourist_spots.urls')),
    path('tourist-spots/', tourist_spots, name='tourist_spots'),
]