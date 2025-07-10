# your_app/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Allergy, BloodGroup, Condition, CustomUser, DoctorProfile, Gender,
    Medication, PatientCondition, PatientMedication, PatientProfile,
    PatientSurgery, Surgery, UserFaceImage
)
from django.contrib.auth.admin import UserAdmin

# --- Inline Admins for Richer Profiles ---
class PatientConditionInline(admin.TabularInline): model = PatientCondition; extra = 1
class PatientMedicationInline(admin.TabularInline): model = PatientMedication; extra = 1
class PatientSurgeryInline(admin.TabularInline): model = PatientSurgery; extra = 1

# --- Main Model Admins ---
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('date_of_birth', 'gender', 'phone_number', 'address', 'emergency_contact_phone', 'profile_picture')}),
        ('Internal IDs', {'fields': ('public_profile_id',)}),
    )
    readonly_fields = ('public_profile_id', 'date_joined', 'last_login')

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'weight_kg', 'height_cm')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    list_select_related = ('user', 'blood_group')
    inlines = [PatientConditionInline, PatientMedicationInline, PatientSurgeryInline]
    autocomplete_fields = ['user'] # Ավելի հարմար է դարձնում user-ի ընտրությունը

@admin.register(UserFaceImage)
class UserFaceImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_preview', 'uploaded_at')
    list_filter = ('user__username', 'uploaded_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('uploaded_at', 'image_preview')

    def image_preview(self, obj):
        # Թույլ է տալիս ադմինկայի ցուցակում տեսնել նկարի փոքր տարբերակը
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'workplace')
    search_fields = ('user__username', 'specialty', 'license_number')
    autocomplete_fields = ['user']

# --- Simple Model Admins (with search fields) ---
class BaseTermAdmin(admin.ModelAdmin): search_fields = ['name']
admin.site.register(Gender, BaseTermAdmin)
admin.site.register(BloodGroup, BaseTermAdmin)
admin.site.register(Condition, BaseTermAdmin)
admin.site.register(Medication, BaseTermAdmin)
admin.site.register(Surgery, BaseTermAdmin)
admin.site.register(Allergy, BaseTermAdmin)

# Այս մոդելների գրանցումը կարելի է թողնել, եթե կա դրանք առանձին կառավարելու կարիք։
admin.site.register(PatientCondition)
admin.site.register(PatientMedication)
admin.site.register(PatientSurgery)