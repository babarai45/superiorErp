from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User, StudentProfile


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
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact administrator.')
        logout(request)
        return redirect('student_login')

    context = {
        'student': student_profile,
        'user': request.user,
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
