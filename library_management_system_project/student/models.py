from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings


class Book(models.Model):
    book_id = models.CharField(max_length=10, primary_key=True, editable=False, default='TEMP')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

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




class BookRequest(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    collection_date = models.DateField(null=True, blank=True)
    collection_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.book.title}"
from django.db import models

class ContactMessage(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    contact_method = models.CharField(max_length=20, choices=[('email', 'Email'), ('phone', 'Phone')])
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.subject}"
