from django.contrib import admin
from .models import Program, Course, CourseEnrollment, Timetable, CourseMaterial, Announcement


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'total_semesters', 'credits_required']
    list_filter = ['department', 'created_at']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Program Information', {
            'fields': ('code', 'name', 'description')
        }),
        ('Academic Details', {
            'fields': ('department', 'total_semesters', 'credits_required')
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'program', 'semester', 'teacher', 'credits', 'status', 'max_students']
    list_filter = ['program', 'semester', 'status', 'created_at']
    search_fields = ['code', 'title']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Course Information', {
            'fields': ('code', 'title', 'description')
        }),
        ('Academic Details', {
            'fields': ('program', 'semester', 'credits', 'pre_requisite')
        }),
        ('Instructor & Resources', {
            'fields': ('teacher', 'syllabus')
        }),
        ('Enrollment Settings', {
            'fields': ('max_students', 'status')
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'course', 'status', 'grade', 'is_passed', 'enrollment_date']
    list_filter = ['course', 'status', 'is_passed', 'enrollment_date']
    search_fields = ['student__user__email', 'course__code', 'student__roll_number']
    readonly_fields = ['enrollment_date']

    fieldsets = (
        ('Enrollment Information', {
            'fields': ('student', 'course', 'enrollment_date', 'status')
        }),
        ('Grade Information', {
            'fields': ('grade', 'gpa_points', 'is_passed')
        }),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['course', 'day', 'start_time', 'end_time', 'room', 'building', 'semester']
    list_filter = ['day', 'semester', 'course__program']
    search_fields = ['course__code', 'room', 'building']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Course & Schedule', {
            'fields': ('course', 'day', 'start_time', 'end_time', 'semester')
        }),
        ('Location', {
            'fields': ('room', 'building')
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'material_type', 'uploaded_by', 'is_visible', 'uploaded_date']
    list_filter = ['material_type', 'is_visible', 'uploaded_date', 'course__program']
    search_fields = ['course__code', 'title']
    readonly_fields = ['uploaded_date', 'updated_date']

    fieldsets = (
        ('Material Information', {
            'fields': ('course', 'title', 'description', 'material_type')
        }),
        ('File & Visibility', {
            'fields': ('file', 'uploaded_by', 'is_visible')
        }),
        ('Timestamps', {'fields': ('uploaded_date', 'updated_date'), 'classes': ('collapse',)}),
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'priority', 'posted_by', 'is_visible', 'posted_date']
    list_filter = ['priority', 'is_visible', 'posted_date']
    search_fields = ['title', 'content']
    readonly_fields = ['posted_date', 'updated_date']

    fieldsets = (
        ('Announcement Information', {
            'fields': ('title', 'content', 'course', 'priority')
        }),
        ('Visibility & Expiration', {
            'fields': ('is_visible', 'posted_by', 'expires_at')
        }),
        ('Timestamps', {'fields': ('posted_date', 'updated_date'), 'classes': ('collapse',)}),
    )

