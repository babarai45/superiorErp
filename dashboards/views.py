from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.utils import timezone
from datetime import timedelta, date

from accounts.models import StudentProfile, TeacherProfile, User
from courses.models import Course, CourseEnrollment, Timetable, Announcement, CourseMaterial
from attendance.models import AttendanceRecord, AttendanceSummary, AttendanceAlert
from grades.models import GradeEntry, SemesterGPA, AssessmentComponent, AssessmentSubmission


# ===== STUDENT DASHBOARD =====

@login_required(login_url='login')
def student_dashboard(request):
    """Student dashboard main view"""
    if request.user.role != 'student':
        return redirect('login')

    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found')
        return redirect('login')

    # Get enrolled courses
    enrollments = CourseEnrollment.objects.filter(student=student, status='enrolled')
    courses = [e.course for e in enrollments]

    # Get attendance summary
    attendance_summary = AttendanceSummary.objects.filter(student=student)

    # Get grades
    grades = GradeEntry.objects.filter(student=student)

    # Get upcoming classes (next 7 days)
    today = date.today()
    next_week = today + timedelta(days=7)
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

    # Get alerts
    alerts = AttendanceAlert.objects.filter(
        student=student,
        is_resolved=False
    ).order_by('-created_at')[:5]

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
        'enrollments': enrollments,
        'courses': courses,
        'attendance_summary': attendance_summary,
        'grades': grades,
        'upcoming_classes': upcoming_classes,
        'announcements': announcements,
        'alerts': alerts,
        'total_classes': total_classes,
        'present_classes': present_classes,
        'avg_attendance': avg_attendance,
        'semester_gpa': semester_gpa,
    }

    return render(request, 'dashboards/student_dashboard.html', context)


@login_required(login_url='login')
def student_courses(request):
    """View all enrolled courses"""
    if request.user.role != 'student':
        return redirect('login')

    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('login')

    enrollments = CourseEnrollment.objects.filter(student=student).select_related('course')

    context = {
        'student': student,
        'enrollments': enrollments,
    }

    return render(request, 'dashboards/student_courses.html', context)


@login_required(login_url='login')
def course_details(request, course_id):
    """View course details including materials and assignments"""
    if request.user.role != 'student':
        return redirect('login')

    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('login')

    course = get_object_or_404(Course, id=course_id)

    # Verify student is enrolled
    enrollment = get_object_or_404(CourseEnrollment, student=student, course=course)

    # Get course materials
    materials = CourseMaterial.objects.filter(course=course, is_visible=True).order_by('-uploaded_date')

    # Get assessments
    assessments = AssessmentComponent.objects.filter(course=course)

    # Get student's submissions
    submissions = AssessmentSubmission.objects.filter(student=student, assessment__course=course)

    # Get grade
    grade = GradeEntry.objects.filter(student=student, course=course).first()

    # Get attendance for this course
    attendance = AttendanceSummary.objects.filter(student=student, course=course).first()

    # Get timetable
    timetable = Timetable.objects.filter(course=course)

    context = {
        'student': student,
        'course': course,
        'enrollment': enrollment,
        'materials': materials,
        'assessments': assessments,
        'submissions': submissions,
        'grade': grade,
        'attendance': attendance,
        'timetable': timetable,
    }

    return render(request, 'dashboards/course_details.html', context)


@login_required(login_url='login')
def student_attendance(request):
    """View attendance details"""
    if request.user.role != 'student':
        return redirect('login')

    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('login')

    # Get enrollment courses
    enrollments = CourseEnrollment.objects.filter(student=student, status='enrolled')
    courses = [e.course for e in enrollments]

    # Get attendance records
    attendance_records = AttendanceRecord.objects.filter(
        student=student
    ).order_by('-date').select_related('course')

    # Get attendance summary
    summary = AttendanceSummary.objects.filter(student=student)

    context = {
        'student': student,
        'attendance_records': attendance_records,
        'summary': summary,
    }

    return render(request, 'dashboards/student_attendance.html', context)


@login_required(login_url='login')
def student_grades(request):
    """View grades and GPA"""
    if request.user.role != 'student':
        return redirect('login')

    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('login')

    # Get grades
    grades = GradeEntry.objects.filter(student=student).order_by('-graded_date')

    # Get semester GPAs
    semester_gpas = SemesterGPA.objects.filter(student=student).order_by('-semester')

    # Calculate current CGPA
    if semester_gpas.exists():
        total_credits = semester_gpas.aggregate(total=Count('total_credits'))['total'] or 0
        avg_gpa = semester_gpas.aggregate(avg=Avg('gpa'))['avg'] or 0
    else:
        total_credits = 0
        avg_gpa = 0

    context = {
        'student': student,
        'grades': grades,
        'semester_gpas': semester_gpas,
        'total_credits': total_credits,
        'cgpa': avg_gpa,
    }

    return render(request, 'dashboards/student_grades.html', context)


# ===== TEACHER DASHBOARD =====

@login_required(login_url='login')
def teacher_dashboard(request):
    """Teacher dashboard main view"""
    if request.user.role != 'teacher':
        return redirect('login')

    try:
        teacher = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        messages.error(request, 'Teacher profile not found')
        return redirect('login')

    # Get taught courses
    courses = Course.objects.filter(teacher=teacher, status='active')

    # Get total students
    total_students = CourseEnrollment.objects.filter(
        course__in=courses,
        status='enrolled'
    ).count()

    # Get pending assignments
    pending_submissions = AssessmentSubmission.objects.filter(
        assessment__course__in=courses,
        status__in=['submitted', 'late_submitted']
    ).count()

    # Get recent announcements
    announcements = Announcement.objects.filter(
        course__in=courses
    ).order_by('-posted_date')[:5]

    context = {
        'teacher': teacher,
        'courses': courses,
        'total_students': total_students,
        'pending_submissions': pending_submissions,
        'announcements': announcements,
    }

    return render(request, 'dashboards/teacher_dashboard.html', context)


@login_required(login_url='login')
def teacher_course_students(request, course_id):
    """View students in a course"""
    if request.user.role != 'teacher':
        return redirect('login')

    try:
        teacher = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        return redirect('login')

    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    # Get enrolled students
    enrollments = CourseEnrollment.objects.filter(
        course=course,
        status='enrolled'
    ).select_related('student')

    # Get attendance summary for students
    attendance_summary = AttendanceSummary.objects.filter(course=course)

    # Get grades
    grades = GradeEntry.objects.filter(course=course).select_related('student')

    context = {
        'teacher': teacher,
        'course': course,
        'enrollments': enrollments,
        'attendance_summary': attendance_summary,
        'grades': grades,
    }

    return render(request, 'dashboards/teacher_course_students.html', context)


@login_required(login_url='login')
def teacher_assessments(request, course_id):
    """Manage assessments for a course"""
    if request.user.role != 'teacher':
        return redirect('login')

    try:
        teacher = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        return redirect('login')

    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    # Get assessments
    assessments = AssessmentComponent.objects.filter(course=course).order_by('due_date')

    # Get submissions
    submissions = AssessmentSubmission.objects.filter(
        assessment__course=course
    ).order_by('-submission_date')

    context = {
        'teacher': teacher,
        'course': course,
        'assessments': assessments,
        'submissions': submissions,
    }

    return render(request, 'dashboards/teacher_assessments.html', context)


@login_required(login_url='login')
def teacher_attendance(request, course_id):
    """Manage attendance for a course"""
    if request.user.role != 'teacher':
        return redirect('login')

    try:
        teacher = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        return redirect('login')

    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    # Get attendance records
    attendance_records = AttendanceRecord.objects.filter(course=course).order_by('-date')

    # Get summary
    summary = AttendanceSummary.objects.filter(course=course)

    context = {
        'teacher': teacher,
        'course': course,
        'attendance_records': attendance_records,
        'summary': summary,
    }

    return render(request, 'dashboards/teacher_attendance.html', context)


# ===== ADMIN DASHBOARD =====

@login_required(login_url='login')
def admin_dashboard(request):
    """Admin dashboard main view"""
    if request.user.role != 'admin':
        return redirect('login')

    # Count users by role
    total_students = User.objects.filter(role='student').count()
    total_teachers = User.objects.filter(role='teacher').count()
    total_staff = User.objects.filter(role='staff').count()

    # Pending approvals
    pending_students = StudentProfile.objects.filter(is_approved=False).count()
    pending_teachers = TeacherProfile.objects.filter(is_approved=False).count()
    pending_staff = StaffProfile.objects.filter(is_approved=False).count()

    # Total courses
    total_courses = Course.objects.count()

    # Recent registrations
    recent_students = StudentProfile.objects.filter(is_approved=False).order_by('-created_at')[:5]
    recent_teachers = TeacherProfile.objects.filter(is_approved=False).order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_staff': total_staff,
        'pending_students': pending_students,
        'pending_teachers': pending_teachers,
        'pending_staff': pending_staff,
        'total_courses': total_courses,
        'recent_students': recent_students,
        'recent_teachers': recent_teachers,
    }

    return render(request, 'dashboards/admin_dashboard.html', context)


@login_required(login_url='login')
def admin_approvals(request, user_type):
    """Manage user approvals"""
    if request.user.role != 'admin':
        return redirect('login')

    if user_type == 'students':
        pending_users = StudentProfile.objects.filter(is_approved=False).order_by('-created_at')
    elif user_type == 'teachers':
        pending_users = TeacherProfile.objects.filter(is_approved=False).order_by('-created_at')
    elif user_type == 'staff':
        from accounts.models import StaffProfile
        pending_users = StaffProfile.objects.filter(is_approved=False).order_by('-created_at')
    else:
        return redirect('admin_dashboard')

    context = {
        'pending_users': pending_users,
        'user_type': user_type,
    }

    return render(request, 'dashboards/admin_approvals.html', context)


@login_required(login_url='login')
def approve_user(request, user_type, user_id):
    """Approve a user"""
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('admin_dashboard')

    if user_type == 'student':
        user_obj = get_object_or_404(StudentProfile, id=user_id)
    elif user_type == 'teacher':
        user_obj = get_object_or_404(TeacherProfile, id=user_id)
    elif user_type == 'staff':
        from accounts.models import StaffProfile
        user_obj = get_object_or_404(StaffProfile, id=user_id)
    else:
        return redirect('admin_dashboard')

    user_obj.is_approved = True
    user_obj.save()

    messages.success(request, f'{user_type.capitalize()} approved successfully')
    return redirect('admin_approvals', user_type=user_type + 's')


from accounts.models import StaffProfile

