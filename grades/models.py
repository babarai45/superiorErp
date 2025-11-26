from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import StudentProfile, TeacherProfile
from courses.models import Course

# Grade Scale/Rubric
class GradeScale(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Grade Scale'
        verbose_name_plural = 'Grade Scales'

    def __str__(self):
        return self.name


# Grade Entry
class GradeEntry(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grade_entries')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grade_entries')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade = models.CharField(max_length=2)  # A, B+, B, etc.
    gpa_points = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(4)])
    graded_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)
    graded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Grade Entry'
        verbose_name_plural = 'Grade Entries'
        unique_together = ('student', 'course')
        ordering = ['-graded_date']

    def calculate_grade(self):
        """Calculate letter grade from marks"""
        marks = self.marks_obtained
        if marks >= 90:
            self.grade = 'A+'
            self.gpa_points = 4.0
        elif marks >= 85:
            self.grade = 'A'
            self.gpa_points = 4.0
        elif marks >= 80:
            self.grade = 'A-'
            self.gpa_points = 3.7
        elif marks >= 75:
            self.grade = 'B+'
            self.gpa_points = 3.3
        elif marks >= 70:
            self.grade = 'B'
            self.gpa_points = 3.0
        elif marks >= 65:
            self.grade = 'B-'
            self.gpa_points = 2.7
        elif marks >= 60:
            self.grade = 'C+'
            self.gpa_points = 2.3
        elif marks >= 55:
            self.grade = 'C'
            self.gpa_points = 2.0
        elif marks >= 50:
            self.grade = 'C-'
            self.gpa_points = 1.7
        elif marks >= 45:
            self.grade = 'D+'
            self.gpa_points = 1.3
        elif marks >= 40:
            self.grade = 'D'
            self.gpa_points = 1.0
        else:
            self.grade = 'F'
            self.gpa_points = 0.0

        self.save()
        return self.grade

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.code}: {self.grade}"


# Assessment Component (Quiz, Assignment, Midterm, Final)
class AssessmentComponent(models.Model):
    COMPONENT_TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('midterm', 'Midterm'),
        ('final', 'Final Exam'),
        ('practical', 'Practical'),
        ('project', 'Project'),
        ('participation', 'Class Participation'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessment_components')
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    total_marks = models.IntegerField(validators=[MinValueValidator(1)])
    weightage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Percentage weight in final grade")
    due_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Assessment Component'
        verbose_name_plural = 'Assessment Components'
        unique_together = ('course', 'component_type', 'name')
        ordering = ['due_date']

    def __str__(self):
        return f"{self.course.code} - {self.name} ({self.weightage}%)"


# Assessment Submission
class AssessmentSubmission(models.Model):
    STATUS_CHOICES = [
        ('not_submitted', 'Not Submitted'),
        ('submitted', 'Submitted'),
        ('late_submitted', 'Late Submitted'),
        ('graded', 'Graded'),
        ('reviewed', 'Reviewed'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='assessment_submissions')
    assessment = models.ForeignKey(AssessmentComponent, on_delete=models.CASCADE, related_name='submissions')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    submission_file = models.FileField(upload_to='submissions/')
    submission_date = models.DateTimeField()
    is_late = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    teacher_comments = models.TextField(blank=True)
    graded_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Assessment Submission'
        verbose_name_plural = 'Assessment Submissions'
        unique_together = ('student', 'assessment')
        ordering = ['-submission_date']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assessment.name}"


# Semester GPA
class SemesterGPA(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='semester_gpas')
    semester = models.IntegerField()
    total_credits = models.IntegerField(default=0)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(4)])
    academic_standing = models.CharField(max_length=50, blank=True)  # Good Standing, Warning, etc.
    calculated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Semester GPA'
        verbose_name_plural = 'Semester GPAs'
        unique_together = ('student', 'semester')
        ordering = ['-semester']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - Semester {self.semester}: {self.gpa}"


# GPA Prediction
class GPAPrediction(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='gpa_prediction')
    current_cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    predicted_cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    prediction_based_on = models.IntegerField(help_text="Number of courses used for prediction")
    confidence_level = models.DecimalField(max_digits=3, decimal_places=2, help_text="Confidence percentage (0-100)")
    calculated_at = models.DateTimeField(auto_now=True)
    recommendations = models.TextField(blank=True)

    class Meta:
        verbose_name = 'GPA Prediction'
        verbose_name_plural = 'GPA Predictions'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - Predicted: {self.predicted_cgpa}"


# Grade Appeal
class GradeAppeal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grade_appeals')
    grade_entry = models.ForeignKey(GradeEntry, on_delete=models.CASCADE, related_name='appeals')
    appeal_reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    review_comments = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='grade_appeals_reviewed')
    new_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    appealed_date = models.DateTimeField(auto_now_add=True)
    reviewed_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Grade Appeal'
        verbose_name_plural = 'Grade Appeals'
        ordering = ['-appealed_date']

    def __str__(self):
        return f"Appeal - {self.student.user.get_full_name()} - {self.status}"

