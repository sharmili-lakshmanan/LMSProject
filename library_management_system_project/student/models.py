from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.crypto import get_random_string



class Book(models.Model):
    book_id = models.CharField(max_length=10, primary_key=True, editable=False, default='TEMP')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.book_id == 'TEMP' or not self.book_id:
            # Generate a new unique book_id (e.g., 6-character alphanumeric)
            while True:
                new_id = get_random_string(6).upper()
                if not Book.objects.filter(book_id=new_id).exists():
                    self.book_id = new_id
                    break
        super().save(*args, **kwargs)   
    def __str__(self):
        return f"{self.book_id} - {self.title}"




# class BookRequest(models.Model):
#     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     requested_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
#     collection_date = models.DateField(null=True, blank=True)
#     collection_time = models.TimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.student.full_name} - {self.book.title}"


class BookRequest(models.Model):
    REQUEST_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Collected', 'Collected'),
        ('Cancelled', 'Cancelled'),
        ('Expired', 'Expired')
    ]
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='book_requests'
    )
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='book_requests'
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=REQUEST_STATUS,
        default='Pending'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_requests'
    )
    collection_date = models.DateField(null=True, blank=True)
    collection_time = models.TimeField(null=True, blank=True)
    collection_deadline = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    issued_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='issued_requests'
    )


    class Meta:
        ordering = ['-requested_at']
        verbose_name = 'Book Request'
        verbose_name_plural = 'Book Requests'
        permissions = [
            ('can_approve_request', 'Can approve book requests'),
            ('can_view_all_requests', 'Can view all book requests'),
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.book.title} ({self.status})"

    def save(self, *args, **kwargs):
        # Auto-set approval timestamp when status changes to Approved
        if self.status == 'Approved' and not self.approved_at:
            self.approved_at = timezone.now()
            
        # Set collection deadline (3 days from approval if not specified)
        if self.status == 'Approved' and not self.collection_deadline:
            self.collection_deadline = timezone.now() + timezone.timedelta(days=3)
            
        # Auto-expire requests past collection deadline
        if (self.collection_deadline and 
            self.status in ['Pending', 'Approved'] and 
            timezone.now() > self.collection_deadline):
            self.status = 'Expired'
            
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.status in ['Pending', 'Approved']

    @property
    def collection_info(self):
        if self.collection_date and self.collection_time:
            return f"{self.collection_date.strftime('%Y-%m-%d')} at {self.collection_time.strftime('%H:%M')}"
        return "Not specified"
    


class ContactMessage(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    contact_method = models.CharField(max_length=20, choices=[('email', 'Email'), ('phone', 'Phone')])
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.subject}"
