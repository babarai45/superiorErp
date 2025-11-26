from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from accounts.models import User, StudentProfile, TeacherProfile, StaffProfile
from courses.models import Program, Course, CourseEnrollment, Timetable, Announcement
from attendance.models import AttendanceRecord, AttendanceSummary
from grades.models import GradeEntry
import random


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create Programs
        programs = [
            Program.objects.create(
                code='BSCS',
                name='BS Computer Science',
                description='A comprehensive program in computer science',
                department='Computer Science',
                total_semesters=8,
                credits_required=120
            ),
            Program.objects.create(
                code='BSDS',
                name='BS Data Science',
                description='A comprehensive program in data science',
                department='Computer Science',
                total_semesters=8,
                credits_required=120
            ),
            Program.objects.create(
                code='BSAI',
                name='BS Artificial Intelligence',
                description='A comprehensive program in AI',
                department='Computer Science',
                total_semesters=8,
                credits_required=120
            ),
        ]
        self.stdout.write(self.style.SUCCESS(f'Created {len(programs)} programs'))

        # Create Admin User
        admin_user, created = User.objects.get_or_create(
            email='admin@superior.edu.pk',
            defaults={
                'username': 'admin',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True,
            }
        )
        if created:
            admin_user.set_password('Admin@123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create Teacher Users and Profiles
        teachers_data = [
            {
                'email': 'shazad_dar@superior.edu.pk',
                'first_name': 'Muhammad',
                'last_name': 'Shazad Dar',
                'department': 'CS',
                'designation': 'Assistant_Professor',
                'cnic': '12345-6789012-3',
            },
            {
                'email': 'ali_khan@superior.edu.pk',
                'first_name': 'Ali',
                'last_name': 'Khan',
                'department': 'IT',
                'designation': 'Lecturer',
                'cnic': '12346-6789012-3',
            },
        ]

        teachers = []
        for teacher_data in teachers_data:
            user, created = User.objects.get_or_create(
                email=teacher_data['email'],
                defaults={
                    'username': teacher_data['email'].split('@')[0],
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'role': 'teacher',
                    'is_verified': True,
                }
            )
            if created:
                user.set_password('Teacher@123')
                user.save()

            teacher_profile, created = TeacherProfile.objects.get_or_create(
                user=user,
                defaults={
                    'official_email': teacher_data['email'],
                    'personal_email': teacher_data['email'].replace('@superior.edu.pk', '@gmail.com'),
                    'cnic': teacher_data['cnic'],
                    'department': teacher_data['department'],
                    'designation': teacher_data['designation'],
                    'qualification': 'MS',
                    'is_approved': True,
                    'is_active': True,
                }
            )
            teachers.append(teacher_profile)

        self.stdout.write(self.style.SUCCESS(f'Created {len(teachers)} teachers'))

        # Create Courses
        courses = []
        program = programs[0]  # BSCS
        for i in range(3):
            course, created = Course.objects.get_or_create(
                code=f'CS{100 + i}',
                defaults={
                    'title': f'Course {i+1}',
                    'description': f'Description for course {i+1}',
                    'program': program,
                    'semester': (i % 4) + 1,
                    'credits': 3,
                    'teacher': teachers[i % len(teachers)],
                    'max_students': 50,
                    'status': 'active',
                }
            )
            courses.append(course)

        self.stdout.write(self.style.SUCCESS(f'Created {len(courses)} courses'))

        # Create Student Users and Profiles
        students = []
        for j in range(5):
            roll_number = f'su92-bscs-s24-{100 + j:03d}'
            email = f'student{j}@superior.edu.pk'

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': roll_number,
                    'first_name': f'Student',
                    'last_name': f'{j+1}',
                    'role': 'student',
                    'is_verified': True,
                }
            )
            if created:
                user.set_password('Student@123')
                user.save()

            student_profile, created = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'roll_number': roll_number,
                    'father_name': f'Father{j+1}',
                    'cnic': f'1234{j}-6789012-{j}',
                    'date_of_birth': date(2004, 1, 15),
                    'gender': 'M' if j % 2 == 0 else 'F',
                    'personal_email': email.replace('@superior.edu.pk', '@gmail.com'),
                    'university_email': email,
                    'whatsapp_number': f'0300123456{j}',
                    'intake': 'fall',
                    'program': 'BSCS',
                    'current_semester': 2,
                    'is_approved': True,
                }
            )
            students.append(student_profile)

        self.stdout.write(self.style.SUCCESS(f'Created {len(students)} students'))

        # Create Course Enrollments
        for student in students:
            for course in courses:
                CourseEnrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={'status': 'enrolled'}
                )

        self.stdout.write(self.style.SUCCESS(f'Created course enrollments'))

        # Create Attendance Records
        for student in students:
            for course in courses:
                for day_offset in range(10):
                    record_date = date.today() - timedelta(days=day_offset)
                    status = random.choice(['present', 'present', 'present', 'absent', 'late'])

                    AttendanceRecord.objects.get_or_create(
                        student=student,
                        course=course,
                        date=record_date,
                        defaults={
                            'status': status,
                            'recorded_by': courses[0].teacher,
                        }
                    )

                # Create Attendance Summary
                summary, created = AttendanceSummary.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'total_classes': 10,
                        'present_count': random.randint(7, 10),
                        'absent_count': random.randint(0, 2),
                        'late_count': random.randint(0, 1),
                        'excused_count': 0,
                    }
                )
                summary.calculate_percentage()

        self.stdout.write(self.style.SUCCESS(f'Created attendance records'))

        # Create Grades
        for student in students:
            for course in courses:
                marks = random.randint(50, 100)
                # Calculate grade based on marks
                if marks >= 90:
                    grade = 'A+'
                    gpa_points = 4.0
                elif marks >= 85:
                    grade = 'A'
                    gpa_points = 4.0
                elif marks >= 80:
                    grade = 'A-'
                    gpa_points = 3.7
                elif marks >= 75:
                    grade = 'B+'
                    gpa_points = 3.3
                elif marks >= 70:
                    grade = 'B'
                    gpa_points = 3.0
                elif marks >= 65:
                    grade = 'B-'
                    gpa_points = 2.7
                elif marks >= 60:
                    grade = 'C+'
                    gpa_points = 2.3
                elif marks >= 55:
                    grade = 'C'
                    gpa_points = 2.0
                elif marks >= 50:
                    grade = 'C-'
                    gpa_points = 1.7
                elif marks >= 45:
                    grade = 'D+'
                    gpa_points = 1.3
                elif marks >= 40:
                    grade = 'D'
                    gpa_points = 1.0
                else:
                    grade = 'F'
                    gpa_points = 0.0

                grade_entry, created = GradeEntry.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'marks_obtained': marks,
                        'grade': grade,
                        'gpa_points': gpa_points,
                        'graded_by': course.teacher,
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'Created grade entries'))

        # Create Timetable Entries
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for course in courses:
            for idx, day in enumerate(days[:2]):
                Timetable.objects.get_or_create(
                    course=course,
                    day=day,
                    start_time='09:00',
                    defaults={
                        'end_time': '10:30',
                        'room': f'Room {100 + idx}',
                        'building': 'Building A',
                        'semester': course.semester,
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'Created timetable entries'))

        # Create Announcements
        for course in courses:
            Announcement.objects.create(
                course=course,
                title=f'Welcome to {course.title}',
                content=f'Welcome to {course.title}. This is an important announcement.',
                posted_by=course.teacher,
                priority='high',
                is_visible=True,
            )

        self.stdout.write(self.style.SUCCESS(f'Created announcements'))

        self.stdout.write(self.style.SUCCESS('✓ Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('\nTest Credentials:'))
        self.stdout.write(f'Admin: admin@superior.edu.pk / Admin@123')
        self.stdout.write(f'Teacher: {teachers_data[0]["email"]} / Teacher@123')
        self.stdout.write(f'Student: {students[0].personal_email} / Student@123')

