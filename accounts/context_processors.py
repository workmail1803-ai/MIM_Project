from tourist_spots.models import PackageBooking


def pending_bookings_count(request):
    """Context processor to add booking notifications for all users"""
    context = {
        'pending_bookings_count': 0,
        'student_notifications_count': 0
    }
    
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            # Admin notification: pending bookings count
            context['pending_bookings_count'] = PackageBooking.objects.filter(status='pending').count()
        else:
            # Student notification: bookings that have been approved/rejected but not yet seen
            context['student_notifications_count'] = PackageBooking.objects.filter(
                user=request.user,
                status__in=['approved', 'rejected'],
                student_notified=False
            ).count()
    
    return context
