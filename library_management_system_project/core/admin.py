
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# def assign_user_ids(modeladmin, request, queryset):
#     count = 0
#     for user in queryset:
#         if not user.user_id and not user.is_staff and user.admission_year:
#             prefix = f"LIB{user.admission_year}"
#             existing = CustomUser.objects.filter(user_id__startswith=prefix).count()
#             user.user_id = f"{prefix}{existing + 1:03d}"
#             user.save()
#             count += 1
#     modeladmin.message_user(request, f"{count} user ID(s) assigned successfully.")

# assign_user_ids.short_description = "Assign Library User ID to selected users"
def assign_user_ids(modeladmin, request, queryset):
    count = 0
    prefix_counter = {}

    for user in queryset:
        if not user.user_id and not user.is_staff and user.admission_year:
            prefix = f"LIB{user.admission_year}"
            
            # initialize counter from DB only once per prefix
            if prefix not in prefix_counter:
                prefix_counter[prefix] = CustomUser.objects.filter(user_id__startswith=prefix).count()

            prefix_counter[prefix] += 1
            new_id = f"{prefix}{prefix_counter[prefix]:03d}"

            # double-check no duplicates
            if not CustomUser.objects.filter(user_id=new_id).exists():
                user.user_id = new_id
                user.save()
                count += 1

    modeladmin.message_user(request, f"{count} user ID(s) assigned successfully.")



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('user_id','admission_number', 'full_name', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'department', 'course')
    actions = [assign_user_ids] 
    
    fieldsets = (
        (None, {'fields': ('user_id','admission_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'phone_number', 'course', 'year', 'department', 'admission_year', 'passout_year')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('admission_number', 'full_name', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields=('user_id',)
    search_fields = ('admission_number', 'email', 'full_name')
    ordering = ('admission_number',)

admin.site.register(CustomUser, CustomUserAdmin)


