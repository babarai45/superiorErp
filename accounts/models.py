from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


# Student Profile
class StudentProfile(models.Model):
    INTAKE_CHOICES = [
        ('fall', 'Fall'),
        ('spring', 'Spring'),
    ]

    PROGRAM_CHOICES = [
        ('BSCS', 'BS Computer Science'),
        ('BSDS', 'BS Data Science'),
        ('BSAI', 'BS Artificial Intelligence'),
        ('BSCYBERSEC', 'BS Cyber Security'),
        ('BSSE', 'BS Software Engineering'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, unique=True)
    father_name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    personal_email = models.EmailField(unique=True)
    university_email = models.EmailField(unique=True)
    whatsapp_number = models.CharField(max_length=20)
    intake = models.CharField(max_length=10, choices=INTAKE_CHOICES)
    program = models.CharField(max_length=20, choices=PROGRAM_CHOICES)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(4)])
    current_semester = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"


# Teacher Profile
class TeacherProfile(models.Model):
    DESIGNATION_CHOICES = [
        ('Lecturer', 'Lecturer'),
        ('Senior_Lecturer', 'Senior Lecturer'),
        ('Assistant_Professor', 'Assistant Professor'),
        ('Associate_Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
        ('HOD', 'Head of Department'),
    ]

    DEPARTMENT_CHOICES = [
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('AI', 'Artificial Intelligence'),
        ('Business', 'Business Administration'),
        ('Engineering', 'Engineering'),
    ]

    QUALIFICATION_CHOICES = [
        ('BS', 'BS (Bachelor of Science)'),
        ('MS', 'MS (Master of Science)'),
        ('PhD', 'PhD (Doctorate)'),
        ('PostDoc', 'Post-Doctorate'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    official_email = models.EmailField(unique=True)
    personal_email = models.EmailField(unique=True)
    cnic = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    specialization = models.CharField(max_length=200, blank=True)
    total_experience = models.IntegerField(default=0, help_text="Years of experience")
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.designation})"


# Staff Profile
class StaffProfile(models.Model):
    DESIGNATION_CHOICES = [
        ('Sweeper', 'Sweeper'),
        ('Guard', 'Guard / Security'),
        ('Clerk', 'Clerk / Administrative'),
        ('Technician', 'Technician'),
        ('Lab_Assistant', 'Lab Assistant'),
        ('Librarian', 'Librarian'),
        ('Accountant', 'Accountant'),
        ('Office_Manager', 'Office Manager'),
        ('Driver', 'Driver'),
        ('Maintenance', 'Maintenance Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    staff_id = models.CharField(max_length=50, unique=True)
    father_name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    join_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staff Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.staff_id})"


# Email Verification Token
class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Email Verification Token'
        verbose_name_plural = 'Email Verification Tokens'

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.user.email} - {self.token[:10]}..."

