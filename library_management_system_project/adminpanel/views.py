from django.shortcuts import render,redirect,get_object_or_404
from core.models import CustomUser
def admin_dashboard(request):
    return render(request,'adminpanel/admin_index.html')
def add_book(request):
    return render(request,'adminpanel/add_book.html')
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

        # Create and save new student
        student = CustomUser.objects.create(
            full_name=full_name,
            email=email,
            course=course,
            year=year,
            department=department,
            phone_number=phone_number,
            admission_number=admission_number,
            admission_year=admission_year,
            passout_year=passout_year,
            is_staff=False  # Ensure they are not treated as admin
        )

        return redirect('view_students') 
    return render(request,'adminpanel/add_student.html')
# Create your views here.
def view_books(request):
    return render(request,'adminpanel/view_books.html')
def edit_book(request):
    return render(request,'adminpanel/edit_book.html')
def delete_book(request):
    return render(request,'adminpanel/delete_book.html')
def view_students(request):
    return render(request,'adminpanel/view_students.html')
def view_issued_books(request):
    return render(request,'adminpanel/view_issued_books.html')
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
def issue_book(request):
    return render(request,'adminpanel/issue_book.html')
def manage_fines(request):
    return render(request,'adminpanel/manage_fines.html')
def view_archived_books(request):
    return render(request,'adminpanel/view_archived_books.html')
def view_students(request):
    students = CustomUser.objects.filter(is_staff=False).order_by('admission_number')
    return render(request, 'adminpanel/view_student.html', {'students': students})
def manage_courses(request):
    return render(request,'adminpanel/manage_courses.html')
def view_request_book(request):
    return render(request,'adminpanel/view_request_book.html')
def manage_years(request):
    return render(request,'adminpanel/manage_years.html')
def update_admin_profile(request):
    return render(request,'adminpanel/update_admin_profile.html')
