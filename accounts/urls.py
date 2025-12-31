from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('travel-history/', views.travel_history, name='travel_history'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    
    # Booking URLs
    path('packages/', views.study_tour_detail, name='packages'),
    path('book-study-tour/', views.book_study_tour, name='book_study_tour'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    # Admin URLs
    path('admin/bookings/', views.admin_booking_management, name='admin_booking_management'),
    path('admin/bookings/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('admin/bookings/pending/<int:booking_id>/', views.pending_booking, name='pending_booking'),
    path('admin/bookings/cancel/<int:booking_id>/', views.cancel_booking_admin, name='cancel_booking_admin'),
    path('admin/bookings/restore/<int:booking_id>/', views.restore_booking, name='restore_booking'),
    path('admin/bookings/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('admin/bookings/approve-all-pending/', views.approve_all_pending, name='approve_all_pending'),
    path('admin/bookings/restore-all-cancelled/', views.restore_all_cancelled, name='restore_all_cancelled'),
    path('admin/bookings/update-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    
    # Contact Message Management URLs
    path('message/read/<int:message_id>/', views.mark_message_read, name='mark_message_read'),
    path('message/replied/<int:message_id>/', views.mark_message_replied, name='mark_message_replied'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    
    # API URLs
    path('api/available-slots/<int:date_id>/', views.get_available_slots, name='get_available_slots'),
    
    # Tourist spots
    path('tourist-spots/', views.tourist_spots, name='tourist_spots'),
]