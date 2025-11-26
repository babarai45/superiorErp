from django.db import models
from accounts.models import StudentProfile
from courses.models import Course

# Attendance Record
class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey('accounts.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        unique_together = ('student', 'course', 'date')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.code} - {self.date}"


# Attendance Summary
class AttendanceSummary(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_summary')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_summary')
    total_classes = models.IntegerField(default=0)
    present_count = models.IntegerField(default=0)
    absent_count = models.IntegerField(default=0)
    late_count = models.IntegerField(default=0)
    excused_count = models.IntegerField(default=0)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_eligible = models.BooleanField(default=True)  # Based on min attendance requirement
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Attendance Summary'
        verbose_name_plural = 'Attendance Summaries'
        unique_together = ('student', 'course')
        ordering = ['-last_updated']

    def calculate_percentage(self):
        if self.total_classes == 0:
            return 0
        self.attendance_percentage = (self.present_count / self.total_classes) * 100
        self.is_eligible = self.attendance_percentage >= 75  # Minimum 75% attendance
        self.save()
        return self.attendance_percentage

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.code} ({self.attendance_percentage}%)"


# Leave Request
class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    LEAVE_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('emergency', 'Emergency'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='leave_requests')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey('accounts.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_date = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.leave_type} ({self.status})"


# Attendance Alert
class AttendanceAlert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('low_attendance', 'Low Attendance'),
        ('absence_pattern', 'Absence Pattern'),
        ('critical', 'Critical Attendance'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_alerts')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_alerts')
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Attendance Alert'
        verbose_name_plural = 'Attendance Alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.alert_type}"

