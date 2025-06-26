from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.contrib import messages
from adminpanel.models import ContactMessage
from django.http import JsonResponse
from django.core.cache import cache

from .models import CustomUser
from .utils import generate_otp, send_otp_email


# Create your views here.
def index(request):
    return render(request, 'core/index.html')
def about(request):
    return render(request, 'core/about.html')
def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent!")
        return redirect('contact')
    return render(request, 'core/contact.html')
    
def catalog(request):
    return render(request, 'core/catalog.html')


#sign up view


# def sign_up(request):
#     if request.method == 'POST':
#         data = request.POST
#         password1 = data.get('password1')
#         password2 = data.get('password2')

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect('sign_up')

#         if CustomUser.objects.filter(admission_number=data.get('admission_number')).exists():
#             messages.error(request, "Admission number already exists.")
#             return redirect('sign_up')

#         if CustomUser.objects.filter(email=data.get('email')).exists():
#             messages.error(request, "Email already registered.")
#             return redirect('sign_up')

#         user = CustomUser(
#             admission_number=data.get('admission_number'),
#             full_name=data.get('full_name'),
#             email=data.get('email'),
#             course=data.get('course'),
#             year=data.get('year') or None,
#             department=data.get('department'),
#             admission_year=data.get('admission-year'),
#             passout_year=data.get('passout-year'),
#             phone_number=data.get('phone_number'),
#         )
#         user.set_password(password1)
#         user.save()


#         messages.success(request, "Account created successfully. Please login.")
#         return redirect('login')

#     return render(request, 'core/sign_up.html')


def sign_up(request):
    if request.method == 'POST':
        data = request.POST
        password1 = data.get('password1')
        password2 = data.get('password2')

        field_errors = {}
        form_data = data.copy()

        # Validate required fields
        required_fields = [
            'admission_number', 'full_name', 'email', 'course',
            'department', 'admission_year', 'passout_year', 'phone_number',
            'password1', 'password2'
        ]

        for field in required_fields:
            if not data.get(field):
                field_errors[field] = f"{field.replace('_', ' ').capitalize()} is required."

        # Password match check
        if password1 and password2 and password1 != password2:
            field_errors['password2'] = "Passwords do not match."

        # Admission number already exists
        if data.get('admission_number') and CustomUser.objects.filter(admission_number=data.get('admission_number')).exists():
            field_errors['admission_number'] = "Admission number already exists."

        # Email already exists
        if data.get('email') and CustomUser.objects.filter(email=data.get('email')).exists():
            field_errors['email'] = "Email already registered."

        if field_errors:
            return render(request, 'core/sign_up.html', {
                'field_errors': field_errors,
                'form_data': form_data
            })

        # Create user
        user = CustomUser.objects.create_user(
            email=data.get('email'),
            password=password1,
            admission_number=data.get('admission_number'),
            full_name=data.get('full_name'),
            course=data.get('course'),
            year=data.get('year') or None,
            department=data.get('department'),
            admission_year=data.get('admission_year'),
            passout_year=data.get('passout_year'),
            phone_number=data.get('phone_number')
        )

        return render(request, 'core/registration_success.html', {'user_id': user.user_id, 'full_name': user.full_name})

    return render(request, 'core/sign_up.html')

def set_password(request):
    return render(request,'emails/set_password_email.html')


## Login view


# def login_page(request):
#     print("CSRF token:", get_token(request))
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if user.is_superuser:
#                 return redirect('admin_dashboard')  # Or your target view for admin users
#             else:
#                 return redirect('student_dashboard')  # Or your target view for students
#         else:
#             messages.error(request, 'Invalid username or password.')
#     return render(request, 'core/login.html')

# def login_page(request):
#     print("CSRF token:", get_token(request))
#     if request.method == 'POST':
#         email = request.POST.get('email')  # renamed for clarity
#         password = request.POST.get('password')
#         user = authenticate(request, username=email, password=password)  # still uses `username` param

#         if user is not None:
#             login(request, user)
#             if user.is_superuser:
#                 return redirect('admin_dashboard')
#             else:
#                 return redirect('student_dashboard')
#         else:
#             messages.error(request, 'Invalid email or password.')
#     return render(request, 'core/login.html')

def login_page(request):
    form_data = {}
    field_errors = {}

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        form_data['email'] = email  # Preserve email input

        if not email:
            field_errors['email'] = 'Email is required.'
        if not password:
            field_errors['password'] = 'Password is required.'

        if not field_errors:
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_superuser:
                    # Prevent admin login from student login page
                    field_errors['email'] = 'Admins must use the admin login page.'
                else:
                    login(request, user)
                    return redirect('student_dashboard')
            else:
                field_errors['email'] = 'Invalid email or password.'
                field_errors['password'] = 'Invalid email or password.'

    return render(request, 'core/login.html', {
        'form_data': form_data,
        'field_errors': field_errors
    })


def otp_verification(request):
    return render(request, 'core/otp_verification.html')

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            otp = generate_otp()
            cache.set(f'otp_{email}', otp, timeout=300)  # 5 minutes
            send_otp_email(email, otp)
            return JsonResponse({'success': True, 'message': 'OTP sent to your email.'})
        else:
            return JsonResponse({'success': False, 'message': 'Email not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        cached_otp = cache.get(f'otp_{email}')
        if cached_otp and otp == cached_otp:
            cache.set(f'otp_verified_{email}', True, timeout=600)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Invalid OTP.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        otp_verified = cache.get(f'otp_verified_{email}')
        if not otp_verified:
            messages.error(request, 'OTP verification failed.')
            return redirect('otp_verification')
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'core/reset_password.html', {'email': email})
        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            cache.delete(f'otp_verified_{email}')
            messages.success(request, 'Password reset successful. Please login.')
            return redirect('login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('otp_verification')
    email = request.GET.get('email', '')
    return render(request, 'core/reset_password.html', {'email': email})

def custom_404_view(request,exception):
    return render(request, 'core/custom_404_view.html', status=404)
def terms_and_conditions(request):
    return render(request, 'core/terms_and_conditions.html')

def admin_login(request):
    field_errors = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email:
            field_errors['email'] = 'Email is required.'
        if not password:
            field_errors['password'] = 'Password is required.'
        if not field_errors:
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                field_errors['email'] = 'Invalid admin credentials.'
    return render(request, 'core/admin_login.html', {'field_errors': field_errors})



