from django.contrib import admin
from .models import ContactMessage,BookRequest,Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author', 'category', 'short_description', 'has_cover_image')
    search_fields = ('title', 'author', 'category')
    list_filter = ('category',)
    readonly_fields = ('cover_image_preview',)

    # To show a shortened description
    def short_description(self, obj):
        return (obj.description[:75] + '...') if len(obj.description) > 75 else obj.description
    short_description.short_description = 'Description'

    # To indicate if a cover image exists
    def has_cover_image(self, obj):
        return bool(obj.cover_image)
    has_cover_image.boolean = True
    has_cover_image.short_description = 'Cover Image?'

    # Optional: Show a preview of the image in the admin form
    def cover_image_preview(self, obj):
        if obj.cover_image:
            return f'<img src="{obj.cover_image.url}" style="max-height: 200px;" />'
        return "No image"
    cover_image_preview.allow_tags = True
    cover_image_preview.short_description = 'Cover Image Preview'
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'email', 'subject', 'contact_method', 'submitted_at')
    search_fields = ('student_name', 'email', 'subject')
    list_filter = ('contact_method', 'submitted_at')



@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'book', 'status', 'requested_at', 'approved_at',
        'collection_date', 'collection_time', 'collected_at'
    )
    list_filter = ('status', 'requested_at', 'collection_date')
    search_fields = ('student__full_name', 'book__title', 'book__author')
    readonly_fields = ('requested_at', 'approved_at', 'collection_deadline', 'collected_at')

    fieldsets = (
        (None, {
            'fields': ('student', 'book', 'status', 'admin_notes', 'rejection_reason')
        }),
        ('Approval Info', {
            'fields': ('approved_by', 'approved_at', 'collection_date', 'collection_time', 'collection_deadline')
        }),
        ('Collection Info', {
            'fields': ('collected_at',)
        }),
    )

