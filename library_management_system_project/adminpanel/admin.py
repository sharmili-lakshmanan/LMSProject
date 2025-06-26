from django.contrib import admin
from .models import DeletedStudent, IssuedBook, ContactMessage, Admin
from student.models import Book

# Register your models here.
from django.contrib import admin
from .models import DeletedStudent

@admin.register(DeletedStudent)
class DeletedStudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'full_name', 'email', 'department', 'admission_year', 'passout_year', 'deleted_at')
    search_fields = ('admission_number', 'full_name', 'email', 'department')
    list_filter = ('department', 'admission_year', 'passout_year')
    ordering = ('-deleted_at',)
@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'get_student_name', 'get_student_email', 'issue_date', 'due_date', 'status', 'collected_at')
    list_filter = ('status', 'issue_date', 'due_date')
    search_fields = ('book__title', 'full_name', 'email')  # Adjust based on your CustomUser fields

    def get_student_name(self, obj):
        return obj.student.full_name if hasattr(obj.student, 'full_name') else obj.student.username
    get_student_name.short_description = 'Student Name'

    def get_student_email(self, obj):
        return obj.student.email
    get_student_email.short_description = 'Student Email'
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'card_number', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'card_number')
    list_filter = ('subject', 'submitted_at')

@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('admin_full_name', 'admin_email', 'admin_phone_number', 'city', 'state')
    search_fields = ('admin_full_name', 'admin_email', 'city', 'state')