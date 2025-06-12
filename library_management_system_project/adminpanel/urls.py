from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_student/', views.add_student, name='add_student'),
    path('change_admin_password/', views.change_admin_password, name='change_admin_password'),
    path('edit_book/', views.edit_book, name='edit_book'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('issue_book/', views.issue_book, name='issue_book'),
    path('manage_courses/',views.manage_courses,name='manage_courses'),
    path('manage_fines/', views.manage_fines, name='manage_fines'),
    path('manage_years/', views.manage_years, name='manage_years'),
    path('update_admin_profile', views.update_admin_profile, name='update_admin_profile'),
    path('view_archived_books/', views.view_archived_books, name='view_archived_books'),
    path('view_books/', views.view_books, name='view_books'),
    path('view_issued_books/', views.view_issued_books, name='view_issued_books'),
    path('view_request_book/', views.view_request_book, name='view_request_book'),
    path('view_students/', views.view_students, name='view_students'),

 ]
