from django.core.management.base import BaseCommand
from admission.models import AdmissionCriteria, SemesterRoadmap

class Command(BaseCommand):
    help = 'Seed admission criteria and semester roadmaps'

    def handle(self, *args, **options):
        # Create admission criteria for each program
        programs_criteria = [
            {
                'program': 'BSCS',
                'min_fsc_marks': 600,
                'min_fsc_percentage': 60,
                'min_matric_percentage': 50,
                'min_aggregate_score': 70,
            },
            {
                'program': 'BSDS',
                'min_fsc_marks': 650,
                'min_fsc_percentage': 65,
                'min_matric_percentage': 50,
                'min_aggregate_score': 75,
            },
            {
                'program': 'BSAI',
                'min_fsc_marks': 700,
                'min_fsc_percentage': 70,
                'min_matric_percentage': 55,
                'min_aggregate_score': 80,
            },
            {
                'program': 'BSCYBERSEC',
                'min_fsc_marks': 650,
                'min_fsc_percentage': 65,
                'min_matric_percentage': 50,
                'min_aggregate_score': 75,
            },
            {
                'program': 'BSSE',
                'min_fsc_marks': 600,
                'min_fsc_percentage': 60,
                'min_matric_percentage': 50,
                'min_aggregate_score': 70,
            },
        ]

        for criteria in programs_criteria:
            AdmissionCriteria.objects.get_or_create(
                program=criteria['program'],
                defaults=criteria
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(programs_criteria)} admission criteria'))

        # Create semester roadmaps for BSCS
        bscs_courses = [
            # Semester 1
            ('BSCS', 1, 'CS101', 'Introduction to Computer Science', 3),
            ('BSCS', 1, 'MTH101', 'Calculus I', 4),
            ('BSCS', 1, 'ENG101', 'English Composition', 3),
            ('BSCS', 1, 'PHY101', 'Physics I', 4),

            # Semester 2
            ('BSCS', 2, 'CS102', 'Programming Fundamentals', 4),
            ('BSCS', 2, 'MTH102', 'Calculus II', 4),
            ('BSCS', 2, 'CHM101', 'Chemistry I', 3),
            ('BSCS', 2, 'CSE101', 'Digital Logic Design', 3),

            # Semester 3
            ('BSCS', 3, 'CS201', 'Data Structures', 3),
            ('BSCS', 3, 'CS202', 'Object Oriented Programming', 3),
            ('BSCS', 3, 'MTH201', 'Linear Algebra', 3),
            ('BSCS', 3, 'CS203', 'Database Systems', 3),

            # Semester 4
            ('BSCS', 4, 'CS204', 'Operating Systems', 3),
            ('BSCS', 4, 'CS205', 'Web Development', 3),
            ('BSCS', 4, 'CS206', 'Computer Networks', 3),
            ('BSCS', 4, 'CS207', 'Software Engineering', 3),

            # Semester 5
            ('BSCS', 5, 'CS301', 'Algorithms', 3),
            ('BSCS', 5, 'CS302', 'Artificial Intelligence', 3),
            ('BSCS', 5, 'CS303', 'Database Management', 3),
            ('BSCS', 5, 'CS304', 'Mobile App Development', 3),

            # Semester 6
            ('BSCS', 6, 'CS305', 'Machine Learning', 3),
            ('BSCS', 6, 'CS306', 'Cloud Computing', 3),
            ('BSCS', 6, 'CS307', 'Cyber Security', 3),
            ('BSCS', 6, 'CS308', 'Project Management', 3),

            # Semester 7
            ('BSCS', 7, 'CS401', 'Advanced Topics', 3),
            ('BSCS', 7, 'CS402', 'Technical Elective 1', 3),
            ('BSCS', 7, 'CS403', 'Capstone Project Part 1', 3),
            ('BSCS', 7, 'CS404', 'Professional Practice', 2),

            # Semester 8
            ('BSCS', 8, 'CS405', 'Technical Elective 2', 3),
            ('BSCS', 8, 'CS406', 'Capstone Project Part 2', 3),
            ('BSCS', 8, 'CS407', 'Ethics in Computing', 2),
            ('BSCS', 8, 'CS408', 'Career Development', 1),
        ]

        created_count = 0
        for program, semester, code, title, credits in bscs_courses:
            obj, created = SemesterRoadmap.objects.get_or_create(
                program=program,
                semester=semester,
                course_code=code,
                defaults={
                    'course_title': title,
                    'credits': credits,
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} semester roadmap entries'))
        self.stdout.write(self.style.SUCCESS('✓ Admission data seeded successfully!'))

