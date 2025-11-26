from django.contrib import admin
from .models import GradeScale, GradeEntry, AssessmentComponent, AssessmentSubmission, SemesterGPA, GPAPrediction, GradeAppeal


@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_default', 'created_at']
    list_filter = ['is_default', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']


@admin.register(GradeEntry)
class GradeEntryAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'course', 'marks_obtained', 'grade', 'gpa_points', 'graded_date']
    list_filter = ['grade', 'course__program', 'graded_date']
    search_fields = ['student__user__email', 'course__code']
    readonly_fields = ['graded_date', 'updated_date']

    fieldsets = (
        ('Student & Course', {
            'fields': ('student', 'course')
        }),
        ('Grade Information', {
            'fields': ('marks_obtained', 'grade', 'gpa_points')
        }),
        ('Grading Details', {
            'fields': ('graded_by', 'remarks')
        }),
        ('Timestamps', {'fields': ('graded_date', 'updated_date'), 'classes': ('collapse',)}),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'


@admin.register(AssessmentComponent)
class AssessmentComponentAdmin(admin.ModelAdmin):
    list_display = ['course', 'component_type', 'name', 'total_marks', 'weightage', 'due_date']
    list_filter = ['component_type', 'course__program', 'due_date']
    search_fields = ['course__code', 'name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Assessment Information', {
            'fields': ('course', 'component_type', 'name', 'description')
        }),
        ('Grading Details', {
            'fields': ('total_marks', 'weightage', 'due_date')
        }),
        ('Creator', {'fields': ('created_by',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(AssessmentSubmission)
class AssessmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'assessment', 'marks_obtained', 'status', 'submission_date', 'is_late']
    list_filter = ['status', 'is_late', 'submission_date']
    search_fields = ['student__user__email', 'assessment__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'submission_date'

    fieldsets = (
        ('Submission Information', {
            'fields': ('student', 'assessment', 'submission_file')
        }),
        ('Submission Details', {
            'fields': ('submission_date', 'is_late', 'status')
        }),
        ('Grading', {
            'fields': ('marks_obtained', 'teacher_comments', 'graded_date')
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'


@admin.register(SemesterGPA)
class SemesterGPAAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'semester', 'gpa', 'total_credits', 'academic_standing', 'calculated_date']
    list_filter = ['semester', 'academic_standing', 'calculated_date']
    search_fields = ['student__user__email']
    readonly_fields = ['calculated_date']

    fieldsets = (
        ('Student & Semester', {
            'fields': ('student', 'semester')
        }),
        ('GPA Information', {
            'fields': ('gpa', 'total_credits', 'academic_standing')
        }),
        ('Timestamp', {'fields': ('calculated_date',)}),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'


@admin.register(GPAPrediction)
class GPAPredictionAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'current_cgpa', 'predicted_cgpa', 'confidence_level', 'calculated_at']
    list_filter = ['calculated_at']
    search_fields = ['student__user__email']
    readonly_fields = ['calculated_at']

    fieldsets = (
        ('Student', {'fields': ('student',)}),
        ('GPA Information', {
            'fields': ('current_cgpa', 'predicted_cgpa', 'confidence_level', 'prediction_based_on')
        }),
        ('Recommendations', {'fields': ('recommendations',)}),
        ('Timestamp', {'fields': ('calculated_at',)}),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'


@admin.register(GradeAppeal)
class GradeAppealAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'get_course', 'status', 'appealed_date', 'reviewed_date']
    list_filter = ['status', 'appealed_date', 'reviewed_date']
    search_fields = ['student__user__email', 'grade_entry__course__code']
    readonly_fields = ['appealed_date', 'reviewed_date']
    date_hierarchy = 'appealed_date'

    fieldsets = (
        ('Appeal Information', {
            'fields': ('student', 'grade_entry', 'appeal_reason')
        }),
        ('Review', {
            'fields': ('status', 'reviewed_by', 'review_comments', 'new_marks', 'reviewed_date')
        }),
        ('Timestamp', {'fields': ('appealed_date',), 'classes': ('collapse',)}),
    )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student Name'

    def get_course(self, obj):
        return obj.grade_entry.course.code
    get_course.short_description = 'Course'

