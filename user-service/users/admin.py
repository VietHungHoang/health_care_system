from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, UserSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name', 
        'role', 'is_active', 'is_verified', 'created_at'
    )
    list_filter = ('role', 'is_active', 'is_verified', 'gender', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name', 'phone_number', 
                'date_of_birth', 'gender', 'address', 'emergency_contact',
                'profile_image'
            )
        }),
        ('Permissions', {
            'fields': (
                'role', 'is_active', 'is_staff', 'is_superuser', 
                'is_verified', 'groups', 'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('last_login_ip',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'role'
            ),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'get_user_role', 'specialization', 'blood_type', 
        'profile_visibility', 'updated_at'
    )
    list_filter = ('profile_visibility', 'user__role', 'updated_at')
    search_fields = (
        'user__email', 'user__first_name', 'user__last_name',
        'specialization', 'license_number'
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'bio', 'website', 'location', 'birth_place')
        }),
        ('Medical Information', {
            'fields': (
                'blood_type', 'allergies', 'medical_history', 
                'current_medications'
            ),
            'classes': ('collapse',)
        }),
        ('Professional Information', {
            'fields': (
                'license_number', 'specialization', 'years_of_experience',
                'education', 'certifications'
            ),
            'classes': ('collapse',)
        }),
        ('Privacy Settings', {
            'fields': ('profile_visibility',)
        }),
    )
    
    def get_user_role(self, obj):
        return obj.user.get_role_display()
    get_user_role.short_description = 'Role'
    get_user_role.admin_order_field = 'user__role'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'ip_address', 'device_info', 'location',
        'is_active', 'created_at', 'last_activity'
    )
    list_filter = ('is_active', 'device_info', 'created_at')
    search_fields = ('user__email', 'ip_address', 'location')
    readonly_fields = ('session_key', 'user_agent', 'created_at', 'last_activity')
    
    def has_add_permission(self, request):
        return False
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


# Customize admin site
admin.site.site_header = "HealthCare System - User Service"
admin.site.site_title = "User Service Admin"
admin.site.index_title = "Welcome to User Service Administration"