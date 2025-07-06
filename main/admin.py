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
)

admin.site.register(Gender)
admin.site.register(BloodGroup)
admin.site.register(Condition)
admin.site.register(Medication)
admin.site.register(Surgery)
admin.site.register(Allergy)
admin.site.register(CustomUser)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(PatientCondition)
admin.site.register(PatientMedication)
admin.site.register(PatientSurgery)
