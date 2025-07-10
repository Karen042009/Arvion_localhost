# your_app/admin.py

from django.contrib import admin
from .models import (
    Allergy,
    BloodGroup,
    Condition,
    CustomUser,
    DoctorProfile,
    Gender,
    Medication,
    PatientCondition,
    PatientMedication,
    PatientProfile,
    PatientSurgery,
    Surgery,
    UserFaceImage 
)

from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

class UserFaceImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'uploaded_at')
    list_filter = ('user', 'uploaded_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('uploaded_at',)

admin.site.register(Gender)
admin.site.register(BloodGroup)
admin.site.register(Condition)
admin.site.register(Medication)
admin.site.register(Surgery)
admin.site.register(Allergy)
admin.site.register(CustomUser, CustomUserAdmin) 
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(PatientCondition)
admin.site.register(PatientMedication)
admin.site.register(PatientSurgery)
admin.site.register(UserFaceImage, UserFaceImageAdmin) 