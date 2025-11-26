from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods


def home(request):
    """
    Homepage view for CampusGPT
    """
    return render(request, 'home.html')


# ===== LOGIN VIEWS =====

def login_view(request):
    """
    Unified login page with role selection
    Routes to login.html with role selection
    """
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'login.html')


def student_login(request):
    """
    Student login view
    Authenticates using roll number and password
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        roll_number = request.POST.get('roll_number', '')
        password = request.POST.get('password', '')

        # Authenticate user (customize based on your User model)
        user = authenticate(request, username=roll_number, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.get_full_name()}!')
            return redirect('student_dashboard')  # Adjust to your dashboard URL
        else:
            messages.error(request, 'Invalid roll number or password')

    return render(request, 'login.html')


def teacher_login(request):
    """
    Teacher login view
    Authenticates using email and password
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # Authenticate user (customize based on your User model)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.get_full_name()}!')
            return redirect('teacher_dashboard')  # Adjust to your dashboard URL
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')


def staff_login(request):
    """
    Staff login view
    Authenticates using staff ID or email and password
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        identifier = request.POST.get('identifier', '')  # Can be staff ID or email
        password = request.POST.get('password', '')

        # Authenticate user (customize based on your User model)
        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.get_full_name()}!')
            return redirect('staff_dashboard')  # Adjust to your dashboard URL
        else:
            messages.error(request, 'Invalid staff ID/email or password')

    return render(request, 'login.html')


# ===== LOGOUT VIEW =====

def logout_view(request):
    """
    Logout view
    Logs out the current user
    """
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


# ===== REGISTRATION VIEWS =====

def student_register(request):
    """
    Student registration view
    Handles student account creation
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name', '')
        roll_number = request.POST.get('roll_number', '')
        father_name = request.POST.get('father_name', '')
        cnic = request.POST.get('cnic', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        gender = request.POST.get('gender', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        whatsapp = request.POST.get('whatsapp', '')
        personal_email = request.POST.get('personal_email', '')
        university_email = request.POST.get('university_email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        intake = request.POST.get('intake', '')
        program = request.POST.get('program', '')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'student_register.html')

        # Validate password strength (minimum 8 characters)
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'student_register.html')

        # Check if user already exists (customize based on your User model)
        # from django.contrib.auth.models import User
        # if User.objects.filter(username=roll_number).exists():
        #     messages.error(request, 'Roll number already registered')
        #     return render(request, 'student_register.html')

        # Create user account
        # user = User.objects.create_user(
        #     username=roll_number,
        #     email=university_email,
        #     password=password,
        #     first_name=full_name.split()[0],
        #     last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
        # )

        # Create student profile (customize based on your Student model)
        # Student.objects.create(
        #     user=user,
        #     roll_number=roll_number,
        #     father_name=father_name,
        #     cnic=cnic,
        #     date_of_birth=date_of_birth,
        #     gender=gender,
        #     address=address,
        #     phone=phone,
        #     whatsapp=whatsapp,
        #     personal_email=personal_email,
        #     intake=intake,
        #     program=program
        # )

        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'student_register.html')


def teacher_register(request):
    """
    Teacher registration view
    Handles teacher account creation
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name', '')
        official_email = request.POST.get('official_email', '')
        personal_email = request.POST.get('personal_email', '')
        phone = request.POST.get('phone', '')
        cnic = request.POST.get('cnic', '')
        department = request.POST.get('department', '')
        designation = request.POST.get('designation', '')
        qualification = request.POST.get('qualification', '')
        address = request.POST.get('address', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'teacher_register.html')

        # Validate password strength
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'teacher_register.html')

        # Create user account
        # user = User.objects.create_user(
        #     username=official_email,
        #     email=official_email,
        #     password=password,
        #     first_name=full_name.split()[0],
        #     last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
        # )

        # Create teacher profile
        # Teacher.objects.create(
        #     user=user,
        #     official_email=official_email,
        #     personal_email=personal_email,
        #     phone=phone,
        #     cnic=cnic,
        #     department=department,
        #     designation=designation,
        #     qualification=qualification,
        #     address=address
        # )

        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'teacher_register.html')


def staff_register(request):
    """
    Staff registration view
    Handles staff/employee account creation
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name', '')
        staff_id = request.POST.get('staff_id', '')
        father_name = request.POST.get('father_name', '')
        cnic = request.POST.get('cnic', '')
        phone = request.POST.get('phone', '')
        designation = request.POST.get('designation', '')
        address = request.POST.get('address', '')
        join_date = request.POST.get('join_date', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'staff_register.html')

        # Validate password strength
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'staff_register.html')

        # Create user account
        # user = User.objects.create_user(
        #     username=staff_id,
        #     email=staff_id,  # Use staff_id as fallback
        #     password=password,
        #     first_name=full_name.split()[0],
        #     last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
        # )

        # Create staff profile
        # Staff.objects.create(
        #     user=user,
        #     staff_id=staff_id,
        #     father_name=father_name,
        #     cnic=cnic,
        #     phone=phone,
        #     designation=designation,
        #     address=address,
        #     join_date=join_date
        # )

        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'staff_register.html')


