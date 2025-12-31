from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-spot/', views.add_tourist_spot, name='add_spot'),
    path('spot/<int:spot_id>/', views.spot_detail, name='spot_detail'),
    path('spot/<int:spot_id>/delete/', views.delete_tourist_spot, name='delete_spot'),
    path('packages/', views.packages, name='packages'),
    path('travel-history/', views.travel_history, name='travel_history'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Change these URLs to avoid conflict with Django admin
    path('spots/update/<int:spot_id>/', views.update_spot, name='update_spot'),
    path('spots/delete/<int:spot_id>/', views.delete_spot, name='delete_spot'),
        path('manage/', views.manage_spots, name='manage_spots'),
    
    # Tour Package URLs
    path('packages/select-category/', views.select_package_category, name='select_package_category'),
    path('packages/add/', views.add_package, name='add_package'),
    path('packages/edit/<int:package_id>/', views.edit_package, name='edit_package'),
    path('packages/delete/<int:package_id>/', views.delete_package, name='delete_package'),
    
    # Category Package URLs
    path('packages/study-tour/', views.study_tour_packages, name='study_tour_packages'),
    path('packages/cycling/', views.cycling_packages, name='cycling_packages'),
    path('packages/university-programs/', views.university_program_packages, name='university_program_packages'),
    
    # Package Booking URLs
    path('packages/book/<int:package_id>/', views.book_package, name='book_package'),
    path('my-bookings/', views.my_package_bookings, name='my_package_bookings'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_package_booking, name='cancel_package_booking'),
    
    # Admin Package Booking Management
    path('admin-bookings/', views.admin_package_bookings, name='admin_package_bookings'),
    path('admin-bookings/approve/<int:booking_id>/', views.approve_package_booking, name='approve_package_booking'),
    path('admin-bookings/reject/<int:booking_id>/', views.reject_package_booking, name='reject_package_booking'),
    
    # Payment URLs
    path('payment/submit/<int:booking_id>/', views.submit_payment, name='submit_payment'),
    path('payment/verify/<int:payment_id>/', views.verify_payment, name='verify_payment'),
    path('payment/reject/<int:payment_id>/', views.reject_payment, name='reject_payment'),
    path('payment/status/<int:booking_id>/', views.get_booking_payment, name='get_booking_payment'),
    
    # Contact Message Management URLs
    path('message/read/<int:message_id>/', views.mark_message_read, name='mark_message_read'),
    path('message/replied/<int:message_id>/', views.mark_message_replied, name='mark_message_replied'),
    path('message/delete/<int:message_id>/', views.delete_contact_message, name='delete_message'),
    
    # Travel Request URLs
    path('travel-request/submit/', views.submit_travel_request, name='submit_travel_request'),
    path('travel-request/my-requests/', views.my_travel_requests, name='my_travel_requests'),
    path('travel-request/admin/', views.admin_travel_requests, name='admin_travel_requests'),
    path('travel-request/approve/<int:request_id>/', views.approve_travel_request, name='approve_travel_request'),
    path('travel-request/reject/<int:request_id>/', views.reject_travel_request, name='reject_travel_request'),
    path('travel-request/delete/<int:request_id>/', views.delete_travel_request, name='delete_travel_request'),
]