from django.contrib import admin
from .models import AttendanceRecord, AttendanceSummary, LeaveRequest, AttendanceAlert


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'get_student_name', 'course', 'status', 'recorded_by', 'recorded_at']
    list_filter = ['status', 'date', 'course__program']
    search_fields = ['student__user__email', 'course__code', 'student__roll_number']
    readonly_fields = ['recorded_at', 'updated_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Attendance Information', {
            'fields': ('student', 'course', 'date', 'status')
        }),
        ('Additional Info', {
            'fields': ('remarks', 'recorded_by')
        }),
        ('Timestamps', {'fields': ('recorded_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'


@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'course', 'total_classes', 'present_count', 'attendance_percentage', 'is_eligible']
    list_filter = ['is_eligible', 'course__program']
    search_fields = ['student__user__email', 'course__code']
    readonly_fields = ['attendance_percentage', 'last_updated']

    fieldsets = (
        ('Student & Course', {
            'fields': ('student', 'course')
        }),
        ('Attendance Statistics', {
            'fields': ('total_classes', 'present_count', 'absent_count', 'late_count', 'excused_count', 'attendance_percentage')
        }),
        ('Status', {'fields': ('is_eligible', 'last_updated')}),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'course', 'leave_type', 'from_date', 'to_date', 'status', 'requested_at']
    list_filter = ['status', 'leave_type', 'from_date', 'course__program']
    search_fields = ['student__user__email', 'course__code']
    readonly_fields = ['requested_at', 'updated_at', 'approval_date']
    date_hierarchy = 'requested_at'

    fieldsets = (
        ('Leave Request Information', {
            'fields': ('student', 'course', 'leave_type', 'from_date', 'to_date', 'reason')
        }),
        ('Approval', {
            'fields': ('status', 'approved_by', 'approval_date', 'rejection_reason')
        }),
        ('Timestamps', {'fields': ('requested_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'


@admin.register(AttendanceAlert)
class AttendanceAlertAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'course', 'alert_type', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'is_resolved', 'created_at']
    search_fields = ['student__user__email', 'course__code']
    readonly_fields = ['created_at', 'resolved_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Alert Information', {
            'fields': ('student', 'course', 'alert_type', 'message')
        }),
        ('Resolution', {'fields': ('is_resolved', 'resolved_at')}),
        ('Timestamp', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'

