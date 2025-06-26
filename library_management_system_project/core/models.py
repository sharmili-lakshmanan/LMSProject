from django.db import models
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Generate user_id for students only
        if not user.is_staff and user.admission_year:
            prefix = f"LIB{user.admission_year}"
            existing = CustomUser.objects.filter(user_id__startswith=prefix).count()
            user.user_id = f"{prefix}{existing + 1:03d}"
            user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, password=password, **extra_fields)


# class CustomUserManager(BaseUserManager):
#     def create_user(self, admission_number, full_name, email, password=None, **extra_fields):
#         if not email or not admission_number:
#             raise ValueError("Email and Admission number are required")
#         email = self.normalize_email(email)
#         user = self.model(admission_number=admission_number, full_name=full_name, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self,full_name, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(full_name, email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     admission_number = models.CharField(max_length=20, unique=True)
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     course = models.CharField(max_length=50)
#     year = models.PositiveIntegerField(null=True, blank=True)
#     department = models.CharField(max_length=50)
#     admission_year = models.PositiveIntegerField()
#     passout_year = models.PositiveIntegerField()
#     phone_number = models.CharField(max_length=15)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'admission_number'
#     REQUIRED_FIELDS = ['email', 'full_name']

#     def __str__(self):
#         return self.full_name
class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True, blank=True, null=True)  # for students only
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default_profile.png', blank=True)
    admission_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    admission_year = models.PositiveIntegerField(blank=True, null=True)
    passout_year = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Admin logs in with email
    REQUIRED_FIELDS = []  # No additional fields required

    def __str__(self):
        return self.email if self.email else "No Email"


