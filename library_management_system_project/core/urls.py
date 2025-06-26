from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('catalog/', views.catalog, name='catalog'),
    path('login/', views.login_page, name='login'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('set_password_email/',views.set_password,name='set_password'),
    path('admin_login/', views.admin_login, name='admin_login'),

]


