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
    
    
    
]