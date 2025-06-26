from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import BookRequest
from adminpanel.models import IssuedBook
from .models import ContactMessage
from django.contrib import messages
from .models import Book
from django.db.models import Q

@login_required 
def student_dashboard(request):
    query = request.GET.get('q', '')           # text input from search bar
    category = request.GET.get('category', '') # selected category from dropdown

    books = Book.objects.all()

    # Search Logic: title or author contains query
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    # Filter Logic: if category is selected
    if category:
        books = books.filter(category=category)

    context = {
        'books': books,
        'query': query,
        'selected_category': category,
        'full_name': request.user.full_name,
        'user_id': request.user.user_id,
        'email': request.user.email,
        'admission_number': request.user.admission_number,
        'course': request.user.course,
    }
    return render(request, 'student/student_dashboard.html', context)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(new_password) < 8 or len(new_password) > 15:
            messages.error(request, "Password must be between 8 and 15 characters.")
        elif check_password(new_password, request.user.password):
            messages.error(request, "New password is the same as the old password. Please choose a different one.")
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Important: keeps user logged in after password change
            messages.success(request, "Your password was changed successfully.")
            return redirect('student_dashboard')  # replace with your desired redirect
    return render(request, 'student/change_password.html')

@login_required
def issued_books(request):
    return render(request, 'student/issued_books.html', {
        'full_name': request.user.full_name,
        'user_id': request.user.user_id,
        'email': request.user.email,
        'admission_number': request.user.admission_number,
        'course': request.user.course,
    })

# def book_request(request):
#     return render(request, 'student/book_request.html', {
#         'full_name': request.user.full_name,
#         'user_id': request.user.user_id,
#         'email': request.user.email,
#         'admission_number': request.user.admission_number,
#         'course': request.user.course,
#     })
@login_required
def report_issue(request):
    return render(request, 'student/report_issue.html', {
        'full_name': request.user.full_name,
        'user_id': request.user.user_id,
        'email': request.user.email,
        'admission_number': request.user.admission_number,
        'course': request.user.course,
    })
@login_required
def contact_librarian(request):
    success = False

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_method = request.POST.get('contactMethod')
        attachment = request.FILES.get('attachment')

        user = request.user
        student_name = user.full_name
        email = user.email

        ContactMessage.objects.create(
            student=user,
            student_name=student_name,
            email=email,
            subject=subject,
            message=message,
            contact_method=contact_method,
            attachment=attachment,
        )

        success = True

    return render(request, 'student/contact_librarian.html', {'success': success,
                                                              
        'full_name': request.user.full_name,
        'user_id': request.user.user_id,})


@login_required
def requested_books(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, book_id=book_id)

        # Check if request already exists to avoid duplicate
        if BookRequest.objects.filter(student=request.user, book=book).exists():
            messages.warning(request, "You've already requested this book.")
        else:
            BookRequest.objects.create(student=request.user, book=book)
            messages.success(request, "Book request submitted successfully!")

        return redirect('student_dashboard')  # or redirect to 'requested_books' page if you prefer

    # GET request — render requested books for the student
    requests = BookRequest.objects.filter(student=request.user).select_related('book')
    return render(request, 'student/requested_books.html', {
        'requests': requests,
        'full_name': request.user.full_name,
        'user_id': request.user.user_id,
        'email': request.user.email,
        'admission_number': request.user.admission_number,
        'course': request.user.course,
    })
    
@login_required
def student_profile(request):
    user = request.user

    if request.method == 'POST':
        new_email = request.POST.get('email')
        new_phone = request.POST.get('phone_number')
        profile_photo = request.FILES.get('profile_photo')

        if new_email:
            user.email = new_email
        if new_phone:
            user.phone_number = new_phone
        if profile_photo:
            user.profile_photo = profile_photo

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('student_profile')  # Replace with your actual URL name

    # Values for non-editable fields
    total_borrowed = user.borrowed_books.count() if hasattr(user, 'borrowed_books') else 0
    current_books = user.borrowed_books.filter(returned=False).count() if hasattr(user, 'borrowed_books') else 0
    fine_balance = user.fine_balance if hasattr(user, 'fine_balance') else 0.00

    context = {
        'full_name': user.full_name,
        'email': user.email,
        'phone_number': user.phone_number,
        'course': user.course,
        'department': user.department,
        'admission_year': user.admission_year,
        'passout_year': user.passout_year,
        'user_id': user.user_id,
        'total_borrowed': total_borrowed,
        'current_books': current_books,
        'fine_balance': fine_balance,
    }

    return render(request, 'student/student_profile.html', context)
  
@login_required
def borrowed_books(request):
    borrowed_books = IssuedBook.objects.filter(
        student=request.user,
        
        status__in=['collected', 'overdue', 'returned', 'due_soon']
    ).order_by('-issue_date')
    
        
        
       
    return render(request, 'student/borrowed_books.html', {'borrowed_books': borrowed_books,
                                                           'full_name': request.user.full_name,
                                                           'user_id': request.user.user_id,
                                                           'email': request.user.email,
                                                           'admission_number': request.user.admission_number,
                                                           'course': request.user.course,})