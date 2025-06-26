from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from core.models import CustomUser
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from datetime import timedelta
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.conf import settings
from .models import IssuedBook, ContactMessage  # update with your actual model import
from django.contrib.auth.decorators import login_required
from student.models import BookRequest,Book
from django.views.generic import ListView
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DeletedStudent
import string
from django.views.decorators.http import require_POST
def admin_dashboard(request):
    total_members = CustomUser.objects.count()
    borrowed_books = IssuedBook.objects.filter(status='collected').count()
    total_books = Book.objects.count()
    new_members = CustomUser.objects.filter(date_joined__month=timezone.now().month).count()  # adjust as needed

    return render(request, 'adminpanel/admin_index.html', {
        'total_members': total_members,
        'borrowed_books': borrowed_books,
        'total_books': total_books,
        'new_members': new_members,
    })
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')
        cover_image = request.FILES.get('cover_image')  # handle uploaded image

        if title and author and category and quantity:
            book = Book(
                title=title,
                author=author,
                description=description,
                category=category,
                quantity=quantity,
                cover_image=cover_image
            )
            book.save()  # `book_id` will be auto-generated
            messages.success(request, "Book added successfully!")
            return redirect('add_book')  # or redirect to view books
        else:
            messages.error(request, "All required fields must be filled.")
            
    return render(request, 'adminpanel/add_book.html')
  

def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_student(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        course = request.POST.get('course')
        year = request.POST.get('year')
        department = request.POST.get('department')
        phone_number = request.POST.get('phone_number')
        admission_number = request.POST.get('admission_number')
        admission_year = request.POST.get('admission_year')
        passout_year = request.POST.get('passout_year')

        # Check for duplicates
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f"Email {email} is already registered.")
            return render(request, 'adminpanel/add_student.html', request.POST)

        if CustomUser.objects.filter(admission_number=admission_number).exists():
            messages.error(request, f"Admission number {admission_number} already exists.")
            return render(request, 'adminpanel/add_student.html', request.POST)

        # Create user with generated user_id
        student = CustomUser.objects.create_user(
            email=email,
            password=None,
            admission_number=admission_number,
            full_name=full_name,
            course=course,
            year=year or None,
            department=department,
            admission_year=admission_year,
            passout_year=passout_year,
            phone_number=phone_number,
            is_staff=False
        )
        student.set_unusable_password()
        student.save()

       
        # Generate temporary password
        temp_password = generate_temp_password()

        # Create user with generated password
        student = CustomUser.objects.create_user(
            email=email,
            password=temp_password,
            admission_number=admission_number,
            full_name=full_name,
            course=course,
            year=year or None,
            department=department,
            admission_year=admission_year,
            passout_year=passout_year,
            phone_number=phone_number,
            is_staff=False
        )

        # Send email with credentials
        subject = "Your EduShelf Login Credentials"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]
        html_content = render_to_string('emails/set_password_email.html', {
            'full_name': full_name,
            'user_id': student.user_id,
            'email': email,
            'temp_password': temp_password,
        })


        msg = EmailMultiAlternatives(subject, html_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(request, f"Student {full_name} added successfully. Password setup link sent to {email}.")
        return redirect('view_students')

    return render(request, 'adminpanel/add_student.html')

# views.py


@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'POST':
        try:
            student = CustomUser.objects.get(pk=student_id)

            # Collect related histories
            # borrowed_books = list(BorrowedBook.objects.filter(student=student).values())
            # book_requests = list(BookRequest.objects.filter(student=student).values())
            # enquiries = list(Enquiry.objects.filter(student=student).values())

            # Save to DeletedStudent
            DeletedStudent.objects.create(
                original_id=student.id,
                admission_number=student.admission_number,
                full_name=student.full_name,
                email=student.email,
                phone_number=student.phone_number,
                course=student.course if student.course else "Unknown",
                department=student.department if student.department else "Unknown",
                admission_year=student.admission_year,
                passout_year=student.passout_year,
                # borrowed_books=borrowed_books,
                # book_requests=book_requests,
                # enquiries=enquiries,
            )

            # Delete actual student and related records
            student.delete()
            return JsonResponse({'success': True})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=400)

def mark_as_collected(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk)
    if request.method == 'POST':
        collected_at = timezone.now()
        book_request.collected_at = collected_at
        book_request.status = 'Collected'
        book_request.save()

        # Issue the book
        issue_date = collected_at.date()
        due_date = issue_date + timedelta(days=14)
        IssuedBook.objects.create(
            book=book_request.book,
            student=book_request.student,
            issue_date=issue_date,
            due_date=due_date,
            collected_at=book_request.collected_at,
            status='collected'
        )

        messages.success(request, 'Book marked as collected and issued.')
        return redirect('book_requests_list')

    return render(request, 'adminpanel/mark_as_collected.html', {'book_request': book_request})

# Create your views here.
def view_books(request):
    books = Book.objects.all()
    return render(request,'adminpanel/view_books.html',{'books':books})
def edit_book(request, id):
    book = get_object_or_404(Book, book_id=id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')
        book.category = request.POST.get('category')
        if 'cover_image' in request.FILES:
            book.cover_image = request.FILES['cover_image']
        book.save()
        return redirect('view_books')  # or wherever you want to go after editing

    return render(request, 'adminpanel/edit_book.html', {'book': book})

def delete_book(request,id):
    book = get_object_or_404(Book, book_id=id)
    if request.method == 'POST':
        book.delete()
        print("POST data:", request.POST)
        messages.success(request, "Book deleted successfully.")
        return redirect('view_books')  # adjust to your book listing URL name
    return redirect('view_books')  # fallback if GET
    
def view_issued_books(request):
    issued_books = IssuedBook.objects.select_related('book', 'student').all().order_by('-issue_date')
    return render(request, 'adminpanel/view_issued_books.html', {'issued_books': issued_books})

def change_admin_password(request):
    return render(request,'adminpanel/change_admin_password.html')
def edit_student(request,id):
    student = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        student.full_name = request.POST.get('full_name')
        student.email = request.POST.get('email')
        student.course = request.POST.get('course')
        student.year = request.POST.get('year')
        student.department = request.POST.get('department')
        student.phone_number = request.POST.get('phone_number')
        student.admission_number = request.POST.get('admission_number')
        student.admission_year = request.POST.get('admission_year')
        student.passout_year = request.POST.get('passout_year')
        student.save()
        return redirect('view_students')  # Redirect to the view listing all students
    return render(request,'adminpanel/edit_student.html',{'students':student})


from .models import IssuedBook  # Ensure you import this

# def issue_book(request, pk):
#     book_request = get_object_or_404(BookRequest, pk=pk)

#     if request.method == 'POST':
#         collection_date = request.POST.get('collection_date')
#         collection_time = request.POST.get('collection_time')
#         if collection_date and collection_time:
#             book_request.collection_date = collection_date
#             book_request.collection_time = collection_time
#             book_request.status = 'Approved'
#             book_request.approved_by = request.user
#             book_request.save()
#             messages.success(request, 'Book request approved with collection date/time')
#             return redirect('book_requests_list')
#         else:
#             messages.error(request, 'Please provide collection date and time.')

#     return render(request, 'adminpanel/issue_book.html', {'book_request': book_request})

from adminpanel.models import IssuedBook
from datetime import timedelta

def issue_book(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk)

    if request.method == 'POST':
        collection_date = request.POST.get('collection_date')
        collection_time = request.POST.get('collection_time')

        if collection_date and collection_time:
            book_request.collection_date = collection_date
            book_request.collection_time = collection_time
            book_request.status = 'Approved'
            book_request.approved_by = request.user
            book_request.save()

            # Create or update IssuedBook
            issue_date = book_request.approved_at.date()
            due_date = issue_date + timedelta(days=14)

            issued_book, created = IssuedBook.objects.update_or_create(
                student=book_request.student,
                book=book_request.book,
                defaults={
                    'collection_date': collection_date,
                    'collection_time': collection_time,
                    'issue_date': issue_date,
                    'due_date': due_date,
                    'status': 'collected' if book_request.status == 'Collected' else 'pending'
                }
            )

            messages.success(request, 'Book request approved and issued.')
            return redirect('book_requests_list')
        else:
            messages.error(request, 'Please provide collection date and time.')

    return render(request, 'adminpanel/issue_book.html', {'book_request': book_request})

@require_POST
def return_book(request, pk):
    issued_book = get_object_or_404(IssuedBook, pk=pk)
    if issued_book.status.lower() == 'approved':
        issued_book.status = 'returned'
        issued_book.save()
        messages.success(request, f"Book {issued_book.book.title} marked as returned.")
    else:
        messages.warning(request, "This book is not in an 'approved' state.")
    return redirect('view_issued_books')

def manage_fines(request):
    return render(request,'adminpanel/manage_fines.html')
def view_archived_books(request):
    return render(request,'adminpanel/view_archived_books.html')
def view_students(request):
    students = CustomUser.objects.filter(is_staff=False).order_by('admission_number')
    return render(request, 'adminpanel/view_student.html', {'students': students})
#to approve book requests

# class BookRequestListView(ListView):
#     model = BookRequest
#     template_name = 'adminpanel/view_requests.html'
#     context_object_name = 'book_requests'
#     paginate_by = 10
    
#     def get_queryset(self):
#         return BookRequest.objects.filter(status='Pending').order_by('-requested_at')

from django.core.paginator import Paginator

def book_requests_list(request):
    book_requests = BookRequest.objects.all().order_by('-requested_at')
    return render(request, 'adminpanel/view_requests.html', {
        'book_requests': book_requests,
    })


def reject_request(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk)
    book_request.status = 'Rejected'
    book_request.save()
    messages.success(request, 'Book request rejected')
    return redirect('book_requests_list')
def manage_courses(request):
    return render(request,'adminpanel/manage_courses.html')
def manage_years(request):
    return render(request,'adminpanel/manage_years.html')
def update_admin_profile(request):
    user = request.user  # assuming admin is logged in

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        user.zip = request.POST.get('zip')
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('update_admin_profile')

    return render(request, 'adminpanel/update_admin_profile.html', {'user': user})


def admin_book_summary(request):
    books = Book.objects.all()
    book_summaries = []
    for book in books:
        total_issued = IssuedBook.objects.filter(book=book, status='borrowed').count()
        total_collected = IssuedBook.objects.filter(book=book, status='collected').count()
        book_summaries.append({
            'book': book,
            'total_quantity': book.quantity,
            'total_issued': total_issued,
            'total_collected': total_collected,
            'current_available': book.quantity - total_issued,
        })

    borrowed_books = IssuedBook.objects.filter(status='borrowed')
    collected_books = IssuedBook.objects.filter(status='collected')

    return render(request, 'adminpanel/book_availability.html', {
        'book_summaries': book_summaries,
        'borrowed_books': borrowed_books,
        'collected_books': collected_books,
    })

def approve_book_request(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk)

    if request.method == 'POST':
        collection_date = request.POST.get('collection_date')
        collection_time = request.POST.get('collection_time')

        if collection_date and collection_time:
            book_request.collection_date = collection_date
            book_request.collection_time = collection_time
            book_request.status = 'Approved'
            book_request.save()
            messages.success(request, 'Book request approved. Awaiting collection by student.')
            return redirect('book_requests_list')
        else:
            messages.error(request, 'Please enter both collection date and time.')

    return render(request, 'adminpanel/approve_book.html', {'book_request': book_request})

def admin_contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-submitted_at')
    return render(request, 'adminpanel/contact_from_home.html', {'messages': messages})
def mark_as_returned(request, pk):
    issued_book = get_object_or_404(IssuedBook, pk=pk)

    if request.method == 'POST':
        issued_book.return_date = timezone.now().date()
        issued_book.status = 'returned'
        issued_book.save()
        messages.success(request, 'Book marked as returned successfully.')

    return redirect('view_issued_books')