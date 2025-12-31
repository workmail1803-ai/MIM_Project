from django.contrib import admin
from .models import StudyTour, TourDate, TourInclusion, StudyTourBooking

@admin.register(StudyTour)
class StudyTourAdmin(admin.ModelAdmin):
    list_display = ['name', 'original_price', 'discounted_price', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ['study_tour', 'start_date', 'end_date', 'available_slots', 'is_available']
    list_filter = ['is_available', 'start_date']
    search_fields = ['study_tour__name']

@admin.register(StudyTourBooking)
class StudyTourBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'study_tour', 'tour_date', 'status', 'booking_date']
    list_filter = ['status', 'booking_date']
    search_fields = ['user__username', 'user__email', 'study_tour__name']
    actions = ['approve_selected', 'cancel_selected']
    
    def approve_selected(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f"{queryset.count()} bookings approved successfully.")
    approve_selected.short_description = "Approve selected bookings"
    
    def cancel_selected(self, request, queryset):
        for booking in queryset:
            booking.tour_date.available_slots += 1
            booking.tour_date.save()
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} bookings cancelled successfully.")
    cancel_selected.short_description = "Cancel selected bookings"

@admin.register(TourInclusion)
class TourInclusionAdmin(admin.ModelAdmin):
    list_display = ['study_tour', 'name']
    list_filter = ['study_tour']
    search_fields = ['name']