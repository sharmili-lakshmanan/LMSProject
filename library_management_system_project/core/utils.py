# utils.py
import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    send_mail(
        'Your EduShelf OTP',
        f'Your OTP for password reset is: {otp}',
        'no-reply@edushelf.com',
        [email],
        fail_silently=False,
    )