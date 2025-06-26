from django.urls import path
from .views import approve_request, reject_request
from . import views
urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_student/', views.add_student, name='add_student'),
    path('change_admin_password/', views.change_admin_password, name='change_admin_password'),
    path('edit_book/<str:id>/', views.edit_book, name='edit_book'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('issue_book/', views.issue_book, name='issue_book'),
    path('manage_courses/',views.manage_courses,name='manage_courses'),
    path('manage_fines/', views.manage_fines, name='manage_fines'),
    path('manage_years/', views.manage_years, name='manage_years'),
    path('update_admin_profile', views.update_admin_profile, name='update_admin_profile'),
    path('view_archived_books/', views.view_archived_books, name='view_archived_books'),
    path('view_books/', views.view_books, name='view_books'),
    path('view_issued_books/', views.view_issued_books, name='view_issued_books'),
    path('issue_book/<int:pk>/', views.issue_book, name='issue_book'),
 #to approve book requests
    path('requests/', views.book_requests_list, name='book_requests_list'),
    path('return_book/<int:pk>/', views.return_book, name='return_book'),
    path('requests/approve/<int:pk>/', views.approve_request, name='approve_book_request'),
    path('requests/reject/<int:pk>/', views.reject_request, name='reject_book_request'),
    path('mark_collected/<int:pk>/', views.mark_as_collected, name='mark_as_collected'),
    path('view_students/', views.view_students, name='view_students'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('delete_book/<str:id>/', views.delete_book, name='delete_book'),
    path('adminpanel/book-availability/', views.admin_book_summary, name='book_availability'),
    path('adminpanel/contact-messages/', views.admin_contact_messages, name='admin_contact_messages'),
    path('issued_books/<int:pk>/return/', views.mark_as_returned, name='mark_as_returned'),

 ]
