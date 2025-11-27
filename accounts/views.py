from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg, Count
from django.utils import timezone
from datetime import timedelta, date

from .models import User, StudentProfile
from courses.models import Course, CourseEnrollment, Timetable, Announcement
from attendance.models import AttendanceSummary
from grades.models import GradeEntry, SemesterGPA


@require_http_methods(["GET", "POST"])
def student_login(request):
    """Student login view"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'accounts/student_login.html')

        # Authenticate user by email instead of username
        try:
            user = User.objects.get(email=email)
            # Check password
            if user.check_password(password) and user.role == 'student' and user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid email or password, or account is inactive.')
                return render(request, 'accounts/student_login.html')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/student_login.html')

    return render(request, 'accounts/student_login.html')


@login_required(login_url='student_login')
def student_dashboard(request):
    """Student dashboard/profile view"""
    try:
        student = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact administrator.')
        logout(request)
        return redirect('student_login')

    # Get enrolled courses
    enrollments = CourseEnrollment.objects.filter(student=student, status='enrolled')
    courses = [e.course for e in enrollments]

    # Get attendance summary
    attendance_summary = AttendanceSummary.objects.filter(student=student)

    # Get grades
    grades = GradeEntry.objects.filter(student=student)

    # Get upcoming classes (next 7 days)
    today = date.today()
    upcoming_classes = Timetable.objects.filter(
        course__in=courses,
        created_at__lte=timezone.now(),
        created_at__gte=timezone.now() - timedelta(days=30)
    ).order_by('day', 'start_time')[:10]

    # Get announcements
    announcements = Announcement.objects.filter(
        Q(course__in=courses) | Q(course__isnull=True),
        is_visible=True
    ).order_by('-posted_date')[:5]

    # Calculate statistics
    total_classes = attendance_summary.aggregate(total=Count('total_classes'))['total'] or 0
    present_classes = attendance_summary.aggregate(total=Count('present_count'))['total'] or 0
    avg_attendance = attendance_summary.aggregate(avg=Avg('attendance_percentage'))['avg'] or 0

    # Get current semester GPA
    semester_gpa = SemesterGPA.objects.filter(
        student=student,
        semester=student.current_semester
    ).first()

    context = {
        'student': student,
        'user': request.user,
        'enrollments': enrollments,
        'courses': courses,
        'attendance_summary': attendance_summary,
        'grades': grades,
        'upcoming_classes': upcoming_classes,
        'announcements': announcements,
        'total_classes': total_classes,
        'present_classes': present_classes,
        'avg_attendance': avg_attendance,
        'semester_gpa': semester_gpa,
    }

    return render(request, 'accounts/student_dashboard.html', context)


@login_required(login_url='student_login')
def student_profile_edit(request):
    """Edit student profile"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('student_dashboard')

    if request.method == 'POST':
        try:
            # Update user info
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            phone = request.POST.get('phone', '').strip()

            if first_name:
                request.user.first_name = first_name
            if last_name:
                request.user.last_name = last_name
            if phone:
                request.user.phone = phone

            # Handle profile image upload
            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                # Check file size (max 5MB)
                if profile_image.size > 5 * 1024 * 1024:
                    messages.error(request, 'Image size must be less than 5MB.')
                    return render(request, 'accounts/student_profile_edit.html', {'student': student_profile})
                request.user.profile_image = profile_image

            request.user.save()

            # Update student profile
            father_name = request.POST.get('father_name', '').strip()
            whatsapp = request.POST.get('whatsapp', '').strip()

            if father_name:
                student_profile.father_name = father_name
            if whatsapp:
                student_profile.whatsapp_number = whatsapp

            student_profile.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('student_dashboard')

        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
            return render(request, 'accounts/student_profile_edit.html', {'student': student_profile})

    context = {
        'student': student_profile,
        'user': request.user,
    }

    return render(request, 'accounts/student_profile_edit.html', context)


@login_required(login_url='student_login')
def student_logout(request):
    """Logout student"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('student_login')
