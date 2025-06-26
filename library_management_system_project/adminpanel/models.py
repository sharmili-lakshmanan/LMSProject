from django.db import models
from django.utils import timezone
from datetime import timedelta
from core.models import CustomUser
from student.models import Book

# Create your models here.
# models.py



class DeletedStudent(models.Model):
    original_id = models.IntegerField()
    admission_number = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    course = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    admission_year = models.IntegerField()
    passout_year = models.IntegerField()
    deleted_at = models.DateTimeField(auto_now_add=True)

    # Additional JSON fields to store history data
    borrowed_books = models.JSONField(default=dict)
    book_requests = models.JSONField(default=dict)
    enquiries = models.JSONField(default=dict)

# models.py
class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    collection_date = models.DateField(null=True, blank=True)
    collection_time = models.TimeField(null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)  # <-- Add this line
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('collected', 'Collected'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ], default='pending')

    def mark_collected(self, collection_date, collection_time):
        self.collection_date = collection_date
        self.collection_time = collection_time
        self.issue_date = collection_date
        self.due_date = collection_date + timedelta(days=14)
        self.return_date = self.due_date  # Set return date as due date by default
        self.collected_at = timezone.now()  # <-- Set collected_at to now
        self.status = 'collected'
        self.save()

    def __str__(self):
        return f"{self.book.title} issued to {self.student.full_name}"

# models.py

class Admin(models.Model):
    # user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='admin_profile')
    admin_profile_photo = models.ImageField(upload_to='admin_photos/', default='admin_photos/default_admin.png', blank=True)
    admin_full_name = models.CharField(max_length=100)
    admin_email = models.EmailField(unique=True)
    admin_phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.full_name

# models.py

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    card_number = models.CharField(max_length=30)
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
