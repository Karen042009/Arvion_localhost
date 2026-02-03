import os, uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


def get_face_image_path(instance, filename):
    """Ֆայլերը պահպանում է media/face/<user_email>/<filename> ճանապարհով։"""
    user_email, user_id_fallback = "unknown", "unknown"
    if isinstance(instance, AbstractUser):
        user_email, user_id_fallback = instance.email, str(instance.id)
    elif hasattr(instance, "user") and instance.user:
        user_email, user_id_fallback = instance.user.email, str(instance.user.id)
    folder_name = user_email if user_email else user_id_fallback
    return os.path.join("face", folder_name, filename)


class Gender(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Անվանում")

    def __str__(self):
        return self.name


class BloodGroup(models.Model):
    group_name = models.CharField(
        max_length=11, unique=True, verbose_name="Խմբի անվանում"
    )

    def __str__(self):
        return self.group_name


class BaseMedicalTerm(models.Model):
    """
    Ընդհանուր բազային կլաս բժշկական տերմինների համար՝ կրկնությունից խուսափելու նպատակով։
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Անվանում")

    class Meta:
        abstract = True  # Այս մոդելի համար բազայում աղյուսակ չի ստեղծվի։
        ordering = ["name"]

    def __str__(self):
        return self.name


class Condition(BaseMedicalTerm):
    class Meta(BaseMedicalTerm.Meta):
        verbose_name = "Հիվանդություն"
        verbose_name_plural = "Հիվանդություններ"


class Medication(BaseMedicalTerm):
    class Meta(BaseMedicalTerm.Meta):
        verbose_name = "Դեղամիջոց"
        verbose_name_plural = "Դեղամիջոցներ"


class Surgery(BaseMedicalTerm):
    class Meta(BaseMedicalTerm.Meta):
        verbose_name = "Վիրահատություն"
        verbose_name_plural = "Վիրահատություններ"


class Allergy(BaseMedicalTerm):
    class Meta(BaseMedicalTerm.Meta):
        verbose_name = "Ալերգիա"
        verbose_name_plural = "Ալերգիաներ"


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name="Ծննդյան ամսաթիվ"
    )
    gender = models.ForeignKey(
        Gender, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Սեռ"
    )
    phone_number = models.CharField(
        max_length=25, blank=True, verbose_name="Հեռախոսահամար"
    )
    address = models.TextField(blank=True, verbose_name="Բնակության հասցե")
    emergency_contact_phone = models.CharField(
        max_length=25, blank=True, verbose_name="Վստահված հեռախոսահամար"
    )
    profile_picture = models.ImageField(
        upload_to=get_face_image_path,
        null=True,
        blank=True,
        verbose_name="Պրոֆիլի նկար",
    )
    public_profile_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="Հանրային ID (QR)"
    )

    def __str__(self):
        return self.get_full_name() or self.username


class UserFaceImage(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="face_images",
        verbose_name="Օգտատեր",
    )
    image = models.ImageField(
        upload_to=get_face_image_path, verbose_name="Ճանաչման նկար"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Վերբեռնման ամսաթիվ"
    )

    class Meta:
        verbose_name = "Դեմքի ճանաչման նկար"
        verbose_name_plural = "Դեմքի ճանաչման նկարներ"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Նկար {self.user.username}-ի համար"


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="doctor_profile",
        verbose_name="Օգտատեր",
    )
    specialty = models.CharField(max_length=100, verbose_name="Մասնագիտություն")
    license_number = models.CharField(
        max_length=50, unique=True, verbose_name="Լիցենզիայի համար"
    )
    workplace = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Աշխատավայր"
    )
    biography = models.TextField(blank=True, null=True, verbose_name="Իմ մասին")

    def __str__(self):
        return f"Բժիշկ՝ {self.user}"


class PatientProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="patient_profile",
        verbose_name="Օգտատեր",
    )
    blood_group = models.ForeignKey(
        BloodGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Արյան խումբ",
    )
    weight_kg = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Քաշ (կգ)"
    )
    height_cm = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Հասակ (սմ)"
    )
    other_notes = models.TextField(blank=True, verbose_name="Այլ նշումներ")
    conditions = models.ManyToManyField(
        Condition, through="PatientCondition", verbose_name="Հիվանդություններ"
    )
    medications = models.ManyToManyField(
        Medication, through="PatientMedication", verbose_name="Դեղամիջոցներ"
    )
    surgeries = models.ManyToManyField(
        Surgery, through="PatientSurgery", verbose_name="Վիրահատություններ"
    )
    allergies = models.ManyToManyField(Allergy, blank=True, verbose_name="Ալերգիաներ")

    def __str__(self):
        return f"Պացիենտ՝ {self.user}"


class PatientCondition(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    condition = models.ForeignKey(
        Condition, on_delete=models.CASCADE, verbose_name="Հիվանդություն"
    )
    diagnosis_date = models.DateField(
        null=True, blank=True, verbose_name="Ախտորոշման ամսաթիվ"
    )

    class Meta:
        unique_together = ("patient", "condition")
        verbose_name = "Պացիենտի հիվանդություն"
        verbose_name_plural = "Պացիենտների հիվանդություններ"

    def __str__(self):
        return f"{self.patient} - {self.condition}"


class PatientMedication(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    medication = models.ForeignKey(
        Medication, on_delete=models.CASCADE, verbose_name="Դեղամիջոց"
    )
    dosage = models.CharField(max_length=100, blank=True, verbose_name="Դեղաչափ")
    start_date = models.DateField(null=True, blank=True, verbose_name="Ընդունման սկիզբ")
    notes = models.TextField(blank=True, verbose_name="Նշումներ")

    class Meta:
        unique_together = ("patient", "medication")
        verbose_name = "Պացիենտի դեղամիջոց"
        verbose_name_plural = "Պացիենտների դեղամիջոցներ"

    def __str__(self):
        return f"{self.patient} - {self.medication.name}"


class PatientSurgery(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    surgery = models.ForeignKey(
        Surgery, on_delete=models.CASCADE, verbose_name="Վիրահատություն"
    )
    surgery_date = models.DateField(
        null=True, blank=True, verbose_name="Վիրահատության ամսաթիվ"
    )
    notes = models.TextField(blank=True, verbose_name="Նշումներ")

    class Meta:
        unique_together = ("patient", "surgery")
        verbose_name = "Պացիենտի վիրահատություն"
        verbose_name_plural = "Պացիենտների վիրահատություններ"

    def __str__(self):
        return f"{self.patient} - {self.surgery.name}"
