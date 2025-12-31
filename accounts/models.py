from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StudyTour(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.IntegerField(default=20)
    max_students = models.IntegerField(default=25)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TourDate(models.Model):
    study_tour = models.ForeignKey(StudyTour, on_delete=models.CASCADE, related_name='dates')
    start_date = models.DateField()
    end_date = models.DateField()
    available_slots = models.IntegerField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.study_tour.name} - {self.start_date} to {self.end_date}"

class TourInclusion(models.Model):
    study_tour = models.ForeignKey(StudyTour, on_delete=models.CASCADE, related_name='inclusions')
    name = models.CharField(max_length=200)
    icon_class = models.CharField(max_length=50, default='fas fa-check')
    
    def __str__(self):
        return self.name

class StudyTourBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', '⏳ Pending'),
        ('confirmed', '✅ Confirmed'),
        ('cancelled', '❌ Cancelled'),
        ('completed', '🎉 Completed'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', '⏳ Pending'),
        ('paid', '💰 Paid'),
        ('partial', '💳 Partial'),
        ('refunded', '🔄 Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study_tour = models.ForeignKey(StudyTour, on_delete=models.CASCADE)
    tour_date = models.ForeignKey(TourDate, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_requirements = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-booking_date']
        unique_together = ['user', 'tour_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.study_tour.name}"
    
    def get_status_badge(self):
        status_colors = {
            'pending': 'warning',
            'confirmed': 'success',
            'cancelled': 'danger',
            'completed': 'info'
        }
        return status_colors.get(self.status, 'secondary')
    
    def get_payment_badge(self):
        payment_colors = {
            'pending': 'warning',
            'paid': 'success',
            'partial': 'info',
            'refunded': 'secondary'
        }
        return payment_colors.get(self.payment_status, 'secondary')


class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('booking', 'Trip Booking'),
        ('information', 'General Information'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_subject_display()}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
