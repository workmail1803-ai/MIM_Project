from .models import PackageBooking

def pending_bookings_count(request):
    """Add pending bookings count to all templates for admin notification"""
    context = {'pending_bookings_count': 0, 'student_notifications_count': 0}
    
    if request.user.is_authenticated:
        # Admin notification: pending bookings
        if request.user.is_staff or request.user.is_superuser:
            context['pending_bookings_count'] = PackageBooking.objects.filter(status='pending').count()
        else:
            # Student notification: bookings that have been approved/rejected but not yet seen
            context['student_notifications_count'] = PackageBooking.objects.filter(
                user=request.user,
                status__in=['approved', 'rejected'],
                student_notified=False
            ).count()
    
    return context
