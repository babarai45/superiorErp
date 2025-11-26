from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
import json
import uuid

from .models import (
    AdmissionApplication,
    PersonalInformation,
    PreviousEducation,
    CourseSelection,
    ProgramDetails,
    PaymentInformation,
    SemesterRoadmap,
    AdmissionCriteria,
)


# Main Admission Page
def admission_main(request):
    """Main admission landing page"""
    programs = [
        {
            'code': 'BSCS',
            'name': 'BS Computer Science',
            'duration': '8 Semesters',
            'description': 'Comprehensive program in Computer Science with focus on software development and algorithms',
            'icon': '💻'
        },
        {
            'code': 'BSDS',
            'name': 'BS Data Science',
            'duration': '8 Semesters',
            'description': 'Advanced program in Data Science with machine learning, analytics, and big data',
            'icon': '📊'
        },
        {
            'code': 'BSAI',
            'name': 'BS Artificial Intelligence',
            'duration': '8 Semesters',
            'description': 'Cutting-edge program in AI with deep learning, NLP, and intelligent systems',
            'icon': '🤖'
        },
        {
            'code': 'BSCYBERSEC',
            'name': 'BS Cyber Security',
            'duration': '8 Semesters',
            'description': 'Specialized program in Cyber Security with network security and cryptography',
            'icon': '🔐'
        },
        {
            'code': 'BSSE',
            'name': 'BS Software Engineering',
            'duration': '8 Semesters',
            'description': 'Professional program in Software Engineering with project management and design patterns',
            'icon': '⚙️'
        },
    ]

    context = {
        'programs': programs,
    }

    return render(request, 'admission/main.html', context)


# Start Application
def start_application(request, program_code=None):
    """Start new admission application"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()

        # Check if email already has application
        if AdmissionApplication.objects.filter(email=email).exists():
            messages.warning(request, 'An application already exists for this email. Please login to continue.')
            return redirect('admission_login')

        # Create new application
        application = AdmissionApplication.objects.create(
            email=email,
            current_stage='stage_1'
        )

        messages.success(request, 'Application created! Please fill in your personal information.')
        return redirect('admission_stage1', app_id=application.application_id)

    context = {
        'program_code': program_code,
    }

    return render(request, 'admission/start.html', context)


# Stage 1: Personal Information
def admission_stage1(request, app_id):
    """Stage 1: Personal Information"""
    application = get_object_or_404(AdmissionApplication, application_id=app_id)

    # Check if already completed
    if application.current_stage not in ['stage_1', 'stage_2', 'stage_3', 'stage_4', 'stage_5']:
        if hasattr(application, 'personal_info'):
            personal_info = application.personal_info
        else:
            personal_info = None
    else:
        personal_info = getattr(application, 'personal_info', None)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        father_name = request.POST.get('father_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        cnic = request.POST.get('cnic')
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')
        address = request.POST.get('address')

        try:
            personal_info, created = PersonalInformation.objects.update_or_create(
                application=application,
                defaults={
                    'full_name': full_name,
                    'father_name': father_name,
                    'date_of_birth': date_of_birth,
                    'gender': gender,
                    'cnic': cnic,
                    'phone': phone,
                    'whatsapp': whatsapp,
                    'address': address,
                }
            )

            application.current_stage = 'stage_2'
            application.save()

            messages.success(request, 'Personal information saved! Moving to Stage 2.')
            return redirect('admission_stage2', app_id=app_id)

        except Exception as e:
            messages.error(request, f'Error saving information: {str(e)}')

    context = {
        'application': application,
        'personal_info': personal_info,
        'stage': 1,
    }

    return render(request, 'admission/stage1.html', context)


# Stage 2: Previous Education
def admission_stage2(request, app_id):
    """Stage 2: Previous Education"""
    application = get_object_or_404(AdmissionApplication, application_id=app_id)

    try:
        previous_education = application.previous_education
    except:
        previous_education = None

    if request.method == 'POST':
        try:
            # Extract form data
            fsc_board = request.POST.get('fsc_board', '').strip()
            fsc_year_str = request.POST.get('fsc_year', '').strip()
            fsc_marks_str = request.POST.get('fsc_marks', '').strip()
            fsc_percentage_str = request.POST.get('fsc_percentage', '').strip()

            matric_board = request.POST.get('matric_board', '').strip()
            matric_year_str = request.POST.get('matric_year', '').strip()
            matric_marks_str = request.POST.get('matric_marks', '').strip()
            matric_percentage_str = request.POST.get('matric_percentage', '').strip()

            # Validate all required fields are filled
            if not all([fsc_board, fsc_year_str, fsc_marks_str, fsc_percentage_str,
                       matric_board, matric_year_str, matric_marks_str, matric_percentage_str]):
                messages.error(request, 'Please fill all required fields.')
                return render(request, 'admission/stage2.html', {
                    'application': application,
                    'previous_education': previous_education,
                    'stage': 2,
                })

            # Convert to appropriate types with validation
            try:
                fsc_year = int(fsc_year_str)
                fsc_marks = float(fsc_marks_str)
                fsc_percentage = float(fsc_percentage_str)
                matric_year = int(matric_year_str)
                matric_marks = float(matric_marks_str)
                matric_percentage = float(matric_percentage_str)

                # Validate ranges
                assert 0 <= fsc_marks <= 1100, 'FSc marks must be between 0 and 1100'
                assert 0 <= fsc_percentage <= 100, 'FSc percentage must be between 0 and 100'
                assert 0 <= matric_marks <= 1050, 'Matric marks must be between 0 and 1050'
                assert 0 <= matric_percentage <= 100, 'Matric percentage must be between 0 and 100'

            except ValueError:
                messages.error(request, 'Invalid number format. Please enter valid numbers.')
                return render(request, 'admission/stage2.html', {
                    'application': application,
                    'previous_education': previous_education,
                    'stage': 2,
                })
            except AssertionError as ae:
                messages.error(request, str(ae))
                return render(request, 'admission/stage2.html', {
                    'application': application,
                    'previous_education': previous_education,
                    'stage': 2,
                })

            # Update or create education record
            previous_education, created = PreviousEducation.objects.update_or_create(
                application=application,
                defaults={
                    'fsc_board': fsc_board,
                    'fsc_year': fsc_year,
                    'fsc_marks': fsc_marks,
                    'fsc_percentage': fsc_percentage,
                    'matric_board': matric_board,
                    'matric_year': matric_year,
                    'matric_marks': matric_marks,
                    'matric_percentage': matric_percentage,
                    'additional_qualifications': request.POST.get('additional_qualifications', ''),
                }
            )

            # Handle file uploads (optional)
            if 'fsc_certificate' in request.FILES:
                previous_education.fsc_certificate = request.FILES['fsc_certificate']
            if 'matric_certificate' in request.FILES:
                previous_education.matric_certificate = request.FILES['matric_certificate']
            if 'cnic_scan' in request.FILES:
                previous_education.cnic_scan = request.FILES['cnic_scan']

            previous_education.save()

            # Update application status
            application.current_stage = 'stage_3'
            application.save()

            messages.success(request, 'Education documents uploaded! Moving to Stage 3.')
            return redirect('admission_stage3', app_id=app_id)

        except Exception as e:
            print(f"Exception in Stage 2: {str(e)}")
            print(f"Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error saving education: {str(e)}')

    context = {
        'application': application,
        'previous_education': previous_education,
        'stage': 2,
    }

    return render(request, 'admission/stage2.html', context)


# Stage 3: Course Selection + Auto-Eligibility Check
def admission_stage3(request, app_id):
    """Stage 3: Course Selection with Auto-Eligibility Check"""
    application = get_object_or_404(AdmissionApplication, application_id=app_id)
    course_selection = getattr(application, 'course_selection', None)

    try:
        previous_education = application.previous_education
    except:
        previous_education = None

    if request.method == 'POST':
        program = request.POST.get('program')
        intake = request.POST.get('intake')

        # Calculate eligibility
        eligibility_score = 0
        meets_criteria = False

        if previous_education:
            # Get criteria for this program
            criteria = AdmissionCriteria.objects.filter(program=program).first()

            if criteria and previous_education.fsc_percentage and previous_education.matric_percentage:
                try:
                    # Get actual percentages
                    fsc_pct = float(previous_education.fsc_percentage)
                    matric_pct = float(previous_education.matric_percentage)

                    # Simple eligibility check: both percentages must meet minimum
                    meets_criteria = (
                        fsc_pct >= float(criteria.min_fsc_percentage) and
                        matric_pct >= float(criteria.min_matric_percentage)
                    )

                    # Calculate eligibility score (simple average)
                    eligibility_score = (fsc_pct + matric_pct) / 2

                except (TypeError, ValueError) as e:
                    print(f"Eligibility calculation error: {str(e)}")
                    meets_criteria = False
                    eligibility_score = 0

        # Save course selection
        course_selection, created = CourseSelection.objects.update_or_create(
            application=application,
            defaults={
                'program': program,
                'intake': intake,
                'eligibility_score': eligibility_score,
                'meets_criteria': meets_criteria,
            }
        )

        # Update application status
        if meets_criteria:
            application.admission_status = 'eligible'
            application.current_stage = 'stage_4'

            # Send eligibility email
            send_eligibility_email(application)
            messages.success(request, f'Congratulations! You are eligible for {program}. Check your email for next steps.')
        else:
            application.admission_status = 'ineligible'
            messages.error(request, 'Sorry, you do not meet the minimum criteria for this program. Please try another program.')

        application.save()

        if meets_criteria:
            return redirect('admission_stage4', app_id=app_id)
        else:
            return redirect('admission_stage3', app_id=app_id)

    programs = [
        ('BSCS', 'BS Computer Science'),
        ('BSDS', 'BS Data Science'),
        ('BSAI', 'BS Artificial Intelligence'),
        ('BSCYBERSEC', 'BS Cyber Security'),
        ('BSSE', 'BS Software Engineering'),
    ]

    context = {
        'application': application,
        'course_selection': course_selection,
        'previous_education': previous_education,
        'programs': programs,
        'stage': 3,
    }

    return render(request, 'admission/stage3.html', context)


# Stage 4: Course Details Review
def admission_stage4(request, app_id):
    """Stage 4: Program Details, Roadmap, and Fee Structure"""
    application = get_object_or_404(AdmissionApplication, application_id=app_id)

    try:
        course_selection = application.course_selection
    except:
        course_selection = None

    try:
        program_details = application.program_details
    except:
        program_details = None

    # Get semester roadmap
    if course_selection:
        roadmap = SemesterRoadmap.objects.filter(program=course_selection.program).order_by('semester')
    else:
        roadmap = []

    if request.method == 'POST':
        agree = request.POST.get('agree_terms') == 'on'

        if not agree:
            messages.error(request, 'You must agree to the terms and conditions.')
            return redirect('admission_stage4', app_id=app_id)

        # Create or update program details
        program_details, created = ProgramDetails.objects.update_or_create(
            application=application,
            defaults={
                'program': course_selection.program,
                'agree_terms': True,
            }
        )

        application.current_stage = 'stage_5'
        application.save()

        messages.success(request, 'Program details confirmed! Proceeding to payment.')
        return redirect('admission_stage5', app_id=app_id)

    # Get program info
    program_info = {
        'BSCS': 'BS Computer Science - 8 Semesters, 120 Credits',
        'BSDS': 'BS Data Science - 8 Semesters, 120 Credits',
        'BSAI': 'BS Artificial Intelligence - 8 Semesters, 120 Credits',
        'BSCYBERSEC': 'BS Cyber Security - 8 Semesters, 120 Credits',
        'BSSE': 'BS Software Engineering - 8 Semesters, 120 Credits',
    }

    context = {
        'application': application,
        'course_selection': course_selection,
        'program_details': program_details,
        'roadmap': roadmap,
        'program_info': program_info.get(course_selection.program if course_selection else '', ''),
        'stage': 4,
        'admission_fee': 15000,
        'semester_fee': 75000,
        'student_card_fee': 5000,
    }

    return render(request, 'admission/stage4.html', context)


# Stage 5: Payment
def admission_stage5(request, app_id):
    """Stage 5: Payment Processing"""
    application = get_object_or_404(AdmissionApplication, application_id=app_id)

    try:
        course_selection = application.course_selection
    except:
        course_selection = None

    try:
        payment_info = application.payment_info
    except:
        payment_info = None

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        # Calculate amounts
        admission_fee = 15000
        first_semester_fee = 75000 / 2  # Half of first semester
        student_card_fee = 5000
        
        # Check if transport option is selected (checkbox)
        transport_option = request.POST.get('transport_option')
        transport_fee = 10000 if transport_option else 0

        total_amount = admission_fee + first_semester_fee + student_card_fee + transport_fee

        # Create payment info
        payment_info, created = PaymentInformation.objects.update_or_create(
            application=application,
            defaults={
                'admission_fee': admission_fee,
                'first_semester_fee': first_semester_fee,
                'student_card_fee': student_card_fee,
                'transport_fee': transport_fee,
                'total_amount': total_amount,
                'payment_method': payment_method,
            }
        )

        # Simulate payment processing
        payment_info.payment_status = 'completed'
        payment_info.payment_date = application.updated_at = timezone.now()
        payment_info.save()

        # Generate roll number and email
        generate_student_credentials(application)

        # Send confirmation email
        send_admission_confirmation_email(application)

        application.admission_status = 'approved'
        application.submitted_at = timezone.now()
        application.save()

        messages.success(request, 'Payment successful! Check your email for credentials and next steps.')
        return redirect('admission_confirmation', app_id=app_id)

    context = {
        'application': application,
        'course_selection': course_selection,
        'payment_info': payment_info,
        'stage': 5,
    }

    return render(request, 'admission/stage5.html', context)


# Confirmation Page
def admission_confirmation(request, app_id):
    """Admission Confirmation Page"""
    application = get_object_or_404(AdmissionApplication, application_id=app_id)

    try:
        personal_info = application.personal_info
    except:
        personal_info = None

    try:
        course_selection = application.course_selection
    except:
        course_selection = None

    try:
        payment_info = application.payment_info
    except:
        payment_info = None

    context = {
        'application': application,
        'personal_info': personal_info,
        'course_selection': course_selection,
        'payment_info': payment_info,
    }

    return render(request, 'admission/confirmation.html', context)


# Helper Functions
def send_eligibility_email(application):
    """Send eligibility confirmation email"""
    try:
        subject = f'Great News! You are Eligible - Application {application.application_id}'
        message = f"""
        Dear Applicant,
        
        Congratulations! Your application {application.application_id} has been reviewed and you meet the eligibility criteria.
        
        Your eligibility score: {application.course_selection.eligibility_score:.2f}
        
        Next Steps:
        1. Complete your application by reviewing program details
        2. Proceed with payment
        3. Receive your student credentials
        
        To continue, click the link below:
        {settings.SITE_URL}/admission/stage4/{application.application_id}/
        
        Best regards,
        CampusGPT Admissions Team
        """

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [application.email])
    except Exception as e:
        print(f"Error sending email: {str(e)}")


def generate_student_credentials(application):
    """Generate roll number and university email"""
    course_selection = application.course_selection

    # Generate roll number format: su92-bscs-s24-001
    year_code = date.today().year % 100  # Last 2 digits of year
    semester = 'fall' if course_selection.intake == 'fall' else 'spring'
    semester_code = 's24' if date.today().month <= 6 else 's24'

    # Get count to generate sequential ID
    count = AdmissionApplication.objects.filter(
        admission_status='approved'
    ).count()

    roll_number = f"su{year_code}-{course_selection.program.lower()}-{semester_code}-{count + 1:03d}"
    university_email = f"student.{roll_number}@superior.edu.pk"

    application.roll_number = roll_number
    application.university_email = university_email
    application.save()


def send_admission_confirmation_email(application):
    """Send final admission confirmation"""
    try:
        personal_info = application.personal_info
        course_selection = application.course_selection

        subject = f'Admission Confirmed - {application.roll_number}'
        message = f"""
        Dear {personal_info.full_name},
        
        Congratulations! Your admission to {course_selection.program} has been confirmed!
        
        Your Student Credentials:
        Roll Number: {application.roll_number}
        University Email: {application.university_email}
        Program: {course_selection.program}
        Intake: {course_selection.intake.upper()}
        
        Login Details:
        Email: {application.university_email}
        Initial Password: You will receive this via separate email
        
        Next Steps:
        1. Visit the student portal: {settings.SITE_URL}/login/
        2. Login with your credentials
        3. Complete your profile setup
        4. Access your timetable and course materials
        
        If you have any questions, contact admissions@superior.edu.pk
        
        Best regards,
        CampusGPT Admissions Team
        """

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [application.email])
    except Exception as e:
        print(f"Error sending confirmation email: {str(e)}")


# Login to Continue Application
def admission_login(request):
    """Login to continue existing application"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        application = AdmissionApplication.objects.filter(email=email).first()

        if not application:
            messages.error(request, 'No application found for this email.')
            return redirect('admission_login')

        # Redirect to current stage
        stage_map = {
            'stage_1': 'admission_stage1',
            'stage_2': 'admission_stage2',
            'stage_3': 'admission_stage3',
            'stage_4': 'admission_stage4',
            'stage_5': 'admission_stage5',
            'completed': 'admission_confirmation',
        }

        next_url = stage_map.get(application.current_stage, 'admission_main')
        return redirect(next_url, app_id=application.application_id)

    return render(request, 'admission/login.html')


from django.utils import timezone

