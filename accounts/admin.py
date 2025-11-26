from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, TeacherProfile, StaffProfile, EmailVerificationToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'get_full_name', 'role', 'is_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'address', 'profile_image')}),
        ('Role & Verification', {'fields': ('role', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'get_student_name', 'program', 'intake', 'current_semester', 'cgpa', 'is_approved']
    list_filter = ['program', 'intake', 'current_semester', 'is_approved', 'created_at']
    search_fields = ['roll_number', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Personal Information', {
            'fields': ('roll_number', 'father_name', 'cnic', 'date_of_birth', 'gender', 'address')
        }),
        ('Contact Information', {
            'fields': ('personal_email', 'university_email', 'whatsapp_number')
        }),
        ('Academic Information', {
            'fields': ('intake', 'program', 'current_semester', 'cgpa')
        }),
        ('Approval Status', {'fields': ('is_approved',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_student_name(self, obj):
        return obj.user.get_full_name()
    get_student_name.short_description = 'Student Name'


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['get_teacher_name', 'official_email', 'department', 'designation', 'is_approved', 'is_active']
    list_filter = ['department', 'designation', 'is_approved', 'is_active', 'created_at']
    search_fields = ['official_email', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Personal Information', {
            'fields': ('cnic', 'specialization', 'total_experience')
        }),
        ('Official Information', {
            'fields': ('official_email', 'personal_email', 'department', 'designation', 'qualification')
        }),
        ('Status', {'fields': ('is_approved', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_teacher_name(self, obj):
        return obj.user.get_full_name()
    get_teacher_name.short_description = 'Teacher Name'


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'get_staff_name', 'designation', 'join_date', 'is_approved', 'is_active']
    list_filter = ['designation', 'is_approved', 'is_active', 'join_date']
    search_fields = ['staff_id', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Personal Information', {
            'fields': ('staff_id', 'father_name', 'cnic', 'address')
        }),
        ('Official Information', {
            'fields': ('designation', 'join_date')
        }),
        ('Status', {'fields': ('is_approved', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_staff_name(self, obj):
        return obj.user.get_full_name()
    get_staff_name.short_description = 'Staff Name'


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_used', 'is_valid', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at']

    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Is Valid'

