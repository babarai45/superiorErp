from django.contrib import admin
from .models import (
    AdmissionApplication,
    PersonalInformation,
    PreviousEducation,
    CourseSelection,
    ProgramDetails,
    PaymentInformation,
    SemesterRoadmap,
    AdmissionCriteria,
)


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_id', 'email', 'current_stage', 'admission_status', 'payment_status', 'created_at']
    list_filter = ['current_stage', 'admission_status', 'payment_status', 'created_at']
    search_fields = ['application_id', 'email', 'roll_number']
    readonly_fields = ['application_id', 'created_at', 'updated_at', 'submitted_at', 'approved_at']

    fieldsets = (
        ('Application Info', {'fields': ('application_id', 'email', 'roll_number', 'university_email')}),
        ('Status', {'fields': ('current_stage', 'admission_status', 'payment_status')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'submitted_at', 'approved_at')}),
    )


@admin.register(PersonalInformation)
class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'cnic', 'date_of_birth', 'gender']
    search_fields = ['full_name', 'cnic', 'application__application_id']

    fieldsets = (
        ('Personal Details', {
            'fields': ('application', 'full_name', 'father_name', 'gender', 'date_of_birth')
        }),
        ('Contact', {
            'fields': ('cnic', 'phone', 'whatsapp', 'address')
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(PreviousEducation)
class PreviousEducationAdmin(admin.ModelAdmin):
    list_display = ['application', 'fsc_percentage', 'matric_percentage']
    search_fields = ['application__application_id']

    fieldsets = (
        ('FSc Information', {
            'fields': ('application', 'fsc_board', 'fsc_year', 'fsc_marks', 'fsc_percentage', 'fsc_certificate')
        }),
        ('Matric Information', {
            'fields': ('matric_board', 'matric_year', 'matric_marks', 'matric_percentage', 'matric_certificate')
        }),
        ('Other', {
            'fields': ('additional_qualifications', 'cnic_scan')
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(CourseSelection)
class CourseSelectionAdmin(admin.ModelAdmin):
    list_display = ['application', 'program', 'intake', 'eligibility_score', 'meets_criteria']
    list_filter = ['program', 'intake', 'meets_criteria']
    search_fields = ['application__application_id']

    fieldsets = (
        ('Application', {'fields': ('application',)}),
        ('Course Info', {'fields': ('program', 'intake')}),
        ('Eligibility', {'fields': ('eligibility_score', 'meets_criteria')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(ProgramDetails)
class ProgramDetailsAdmin(admin.ModelAdmin):
    list_display = ['application', 'program', 'agree_terms']
    search_fields = ['application__application_id']

    fieldsets = (
        ('Application', {'fields': ('application',)}),
        ('Program Info', {'fields': ('program', 'program_duration_semesters', 'total_credits')}),
        ('Fee Structure', {
            'fields': ('admission_fee', 'semester_fee', 'student_card_fee', 'transport_fee')
        }),
        ('Roadmap', {'fields': ('semester_roadmap',)}),
        ('Agreement', {'fields': ('agree_terms',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(PaymentInformation)
class PaymentInformationAdmin(admin.ModelAdmin):
    list_display = ['psid', 'application', 'total_amount', 'payment_status', 'payment_method']
    list_filter = ['payment_status', 'payment_method', 'payment_date']
    search_fields = ['psid', 'application__application_id', 'transaction_id']
    readonly_fields = ['psid', 'created_at', 'updated_at']

    fieldsets = (
        ('Payment ID', {'fields': ('psid', 'application')}),
        ('Fees', {
            'fields': ('admission_fee', 'first_semester_fee', 'student_card_fee', 'transport_fee', 'total_amount')
        }),
        ('Payment Method', {'fields': ('payment_method', 'payment_status')}),
        ('Transaction', {'fields': ('transaction_id', 'payment_date')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(SemesterRoadmap)
class SemesterRoadmapAdmin(admin.ModelAdmin):
    list_display = ['program', 'semester', 'course_code', 'course_title', 'credits']
    list_filter = ['program', 'semester']
    search_fields = ['program', 'course_code', 'course_title']

    fieldsets = (
        ('Course Info', {
            'fields': ('program', 'semester', 'course_code', 'course_title', 'credits')
        }),
    )


@admin.register(AdmissionCriteria)
class AdmissionCriteriaAdmin(admin.ModelAdmin):
    list_display = ['program', 'min_fsc_percentage', 'min_matric_percentage', 'min_aggregate_score']
    list_filter = ['program']

    fieldsets = (
        ('Program', {'fields': ('program',)}),
        ('Criteria', {
            'fields': ('min_fsc_marks', 'min_fsc_percentage', 'min_matric_percentage', 'min_aggregate_score')
        }),
    )

