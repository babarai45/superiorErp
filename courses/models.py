from django.db import models
from accounts.models import TeacherProfile, StudentProfile

# Program Model
class Program(models.Model):
    PROGRAM_CHOICES = [
        ('BSCS', 'BS Computer Science'),
        ('BSDS', 'BS Data Science'),
        ('BSAI', 'BS Artificial Intelligence'),
        ('BSCYBERSEC', 'BS Cyber Security'),
        ('BSSE', 'BS Software Engineering'),
    ]

    code = models.CharField(max_length=20, choices=PROGRAM_CHOICES, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=100)
    total_semesters = models.IntegerField(default=8)
    credits_required = models.IntegerField(default=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'
        ordering = ['code']

    def __str__(self):
        return self.name


# Course Model
class Course(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]

    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')
    semester = models.IntegerField()
    credits = models.IntegerField(default=3)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_taught')
    pre_requisite = models.CharField(max_length=100, blank=True)
    syllabus = models.FileField(upload_to='syllabi/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    max_students = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['code']
        unique_together = ('code', 'program', 'semester')

    def __str__(self):
        return f"{self.code} - {self.title}"


# Course Enrollment
class CourseEnrollment(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('deferred', 'Deferred'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    grade = models.CharField(max_length=2, blank=True, null=True)
    gpa_points = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    is_passed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Course Enrollment'
        verbose_name_plural = 'Course Enrollments'
        unique_together = ('student', 'course')
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.code}"


# Timetable Entry
class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable')
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    semester = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Timetable'
        verbose_name_plural = 'Timetables'
        ordering = ['day', 'start_time']
        unique_together = ('course', 'day', 'start_time')

    def __str__(self):
        return f"{self.course.code} - {self.day} {self.start_time}-{self.end_time}"


# Course Materials
class CourseMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('lecture', 'Lecture Notes'),
        ('presentation', 'Presentation'),
        ('reading', 'Reading Material'),
        ('assignment', 'Assignment'),
        ('solution', 'Solution'),
        ('other', 'Other'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    file = models.FileField(upload_to='course_materials/')
    uploaded_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Course Material'
        verbose_name_plural = 'Course Materials'
        ordering = ['-uploaded_date']

    def __str__(self):
        return f"{self.course.code} - {self.title}"


# Announcement
class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements', blank=True, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-posted_date']

    def __str__(self):
        return f"{self.title} - {self.posted_date.strftime('%Y-%m-%d')}"

