from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

# Admission Application Model
class AdmissionApplication(models.Model):
    STATUS_CHOICES = [
        ('stage_1', 'Stage 1 - Personal Information'),
        ('stage_2', 'Stage 2 - Previous Education'),
        ('stage_3', 'Stage 3 - Course Selection'),
        ('stage_4', 'Stage 4 - Course Details Review'),
        ('stage_5', 'Stage 5 - Payment'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    ADMISSION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('eligible', 'Eligible'),
        ('ineligible', 'Ineligible'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Application ID
    application_id = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(unique=True)

    # Current Stage
    current_stage = models.CharField(max_length=20, choices=STATUS_CHOICES, default='stage_1')
    admission_status = models.CharField(max_length=20, choices=ADMISSION_STATUS_CHOICES, default='pending')

    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    # Payment Status
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')

    roll_number = models.CharField(max_length=50, blank=True, unique=True, null=True)
    university_email = models.EmailField(blank=True)

    class Meta:
        verbose_name = 'Admission Application'
        verbose_name_plural = 'Admission Applications'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.application_id:
            self.application_id = f"APP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.application_id} - {self.email}"


# Stage 1: Personal Information
class PersonalInformation(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    application = models.OneToOneField(AdmissionApplication, on_delete=models.CASCADE, related_name='personal_info')

    full_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    cnic = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Personal Information'

    def __str__(self):
        return f"{self.full_name} - {self.application.application_id}"


# Stage 2: Previous Education
class PreviousEducation(models.Model):
    application = models.OneToOneField(AdmissionApplication, on_delete=models.CASCADE, related_name='previous_education')

    # FSc / HSC Information
    fsc_board = models.CharField(max_length=100, blank=True, null=True)
    fsc_year = models.IntegerField(blank=True, null=True)
    fsc_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1100)])
    fsc_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Matric Information
    matric_board = models.CharField(max_length=100, blank=True, null=True)
    matric_year = models.IntegerField(blank=True, null=True)
    matric_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1050)])
    matric_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Additional Qualifications
    additional_qualifications = models.TextField(blank=True)

    # Documents
    fsc_certificate = models.FileField(upload_to='admission/documents/', blank=True, null=True)
    matric_certificate = models.FileField(upload_to='admission/documents/', blank=True, null=True)
    cnic_scan = models.FileField(upload_to='admission/documents/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Previous Education'

    def __str__(self):
        return f"Education - {self.application.application_id}"


# Stage 3: Course Selection
class CourseSelection(models.Model):
    INTAKE_CHOICES = [('fall', 'Fall'), ('spring', 'Spring')]
    PROGRAM_CHOICES = [
        ('BSCS', 'BS Computer Science'),
        ('BSDS', 'BS Data Science'),
        ('BSAI', 'BS Artificial Intelligence'),
        ('BSCYBERSEC', 'BS Cyber Security'),
        ('BSSE', 'BS Software Engineering'),
    ]

    application = models.OneToOneField(AdmissionApplication, on_delete=models.CASCADE, related_name='course_selection')

    program = models.CharField(max_length=20, choices=PROGRAM_CHOICES)
    intake = models.CharField(max_length=10, choices=INTAKE_CHOICES)

    eligibility_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    meets_criteria = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course Selection'

    def __str__(self):
        return f"{self.program} - {self.application.application_id}"


# Stage 4: Program Details (Course Information, Roadmap, Fee Structure)
class ProgramDetails(models.Model):
    application = models.OneToOneField(AdmissionApplication, on_delete=models.CASCADE, related_name='program_details')

    program = models.CharField(max_length=20)
    program_duration_semesters = models.IntegerField(default=8)
    total_credits = models.IntegerField(default=120)

    # Fee Structure
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2, default=15000)
    semester_fee = models.DecimalField(max_digits=10, decimal_places=2, default=75000)
    student_card_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=10000)

    # Semester Roadmap (stored as JSON)
    semester_roadmap = models.TextField(blank=True)  # JSON format

    agree_terms = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Program Details'

    def __str__(self):
        return f"Program Details - {self.application.application_id}"


# Stage 5: Payment Information
class PaymentInformation(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
        ('cheque', 'Cheque'),
    ]

    application = models.OneToOneField(AdmissionApplication, on_delete=models.CASCADE, related_name='payment_info')

    # Fees
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2)
    first_semester_fee = models.DecimalField(max_digits=10, decimal_places=2)
    student_card_fee = models.DecimalField(max_digits=10, decimal_places=2)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')

    # Payment ID (PSID - Payment Session ID)
    psid = models.CharField(max_length=50, unique=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment Information'

    def save(self, *args, **kwargs):
        if not self.psid:
            self.psid = f"PSID-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment {self.psid}"


# Semester Roadmap (Course Structure)
class SemesterRoadmap(models.Model):
    program = models.CharField(max_length=20)
    semester = models.IntegerField()
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=200)
    credits = models.IntegerField()

    class Meta:
        unique_together = ('program', 'semester', 'course_code')
        verbose_name = 'Semester Roadmap'

    def __str__(self):
        return f"{self.program} - Semester {self.semester} - {self.course_code}"


# Admission Criteria
class AdmissionCriteria(models.Model):
    program = models.CharField(max_length=20, unique=True)
    min_fsc_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    min_fsc_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=60)
    min_matric_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=50)
    min_aggregate_score = models.DecimalField(max_digits=5, decimal_places=2, default=70)

    class Meta:
        verbose_name = 'Admission Criteria'

    def __str__(self):
        return f"Criteria - {self.program}"

