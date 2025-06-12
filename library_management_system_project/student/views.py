from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BookRequest
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
@login_required
def change_password(request):
    return render(request, 'student/change_password.html', {
        'full_name': request.user.full_name,
        'user_id': request.user.user_id,
        'email': request.user.email,
        'admission_number': request.user.admission_number,
        'course': request.user.course,
    })
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
    success = False  # Flag to indicate if the form was submitted

    if request.method == 'POST':
        student_name = request.POST.get('studentName')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_method = request.POST.get('contactMethod')
        attachment = request.FILES.get('attachment')

        ContactMessage.objects.create(
            student_name=student_name,
            email=email,
            subject=subject,
            message=message,
            contact_method=contact_method,
            attachment=attachment,
        )

        success = True  # Set success flag

    return render(request, 'student/contact_librarian.html', {'success': success})
@login_required
def contact_success(request):
    return render(request, 'student/contact_success.html')

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
    return render(request, 'student/student_profile.html', {
        'full_name': request.user.full_name,
        'user_id': request.user.user_id,
        'email': request.user.email,
        'admission_number': request.user.admission_number,
        'course': request.user.course,
        'year': request.user.year,
        'department': request.user.department,
        'admission_year': request.user.admission_year,
        'passout_year': request.user.passout_year,
        'phone_number': request.user.phone_number,
    })
@login_required
def borrowed_books(request):
    return render(request, 'student/borrowed_books.html', {
        'full_name': request.user.full_name,
        'user_id': request.user.user_id,
        'email': request.user.email,
        'admission_number': request.user.admission_number,
        'course': request.user.course,
    })