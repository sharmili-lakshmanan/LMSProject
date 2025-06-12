from django.urls import path
from . import views
urlpatterns = [
    # path('', views.student_dashboard, name='student_dashboard'),
    path('', views.student_dashboard, name='student_dashboard'),

    path('change_password/', views.change_password, name='change_password'),
    path('issued_books/', views.issued_books, name='issued_books'),
    # path('book_request/', views.book_request, name='book_request'),
    path('report_issue/', views.report_issue, name='report_issue'),
    path('contact_librarian/', views.contact_librarian, name='contact_librarian'),
    path('requested_books/', views.requested_books, name='requested_books'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),
    path('contact_success/',views.contact_success,name='contact_success'),
]
