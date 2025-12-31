from django.db import models
from django.contrib.auth.models import User

class TouristSpot(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='tourist_spots/')
    highlights = models.TextField(blank=True)
    travel_info = models.TextField(blank=True)
    best_time = models.TextField(blank=True)
    safety_info = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']


class TourPackage(models.Model):
    CATEGORY_CHOICES = [
        ('study_tour', 'Study Tour'),
        ('cycling', 'Cycling'),
        ('university_program', 'University Program'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='tour_packages/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)  # e.g., "3 Days 2 Nights"
    destination = models.CharField(max_length=200)
    highlights = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='study_tour')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    class Meta:
        ordering = ['-created_at']


class PackageBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='package_bookings')
    
    # Student Information
    student_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    emergency_contact = models.CharField(max_length=20, blank=True)
    
    # Booking Details
    num_persons = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    student_notified = models.BooleanField(default=False)  # Track if student has seen the status update
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student_name} - {self.package.name} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    booking = models.ForeignKey(PackageBooking, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    bkash_last_4 = models.CharField(max_length=4)  # Last 4 digits of bKash number
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def payment_percentage(self):
        """Calculate payment percentage of total package price"""
        if self.booking and self.booking.package and self.booking.package.price > 0:
            return round((float(self.amount_paid) / float(self.booking.package.price)) * 100, 1)
        return 0
    
    def __str__(self):
        return f"Payment for {self.booking.student_name} - {self.amount_paid} (Status: {self.status})"
    
    class Meta:
        ordering = ['-created_at']