from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Gender(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Անվանում")

    def __str__(self):
        return self.name


class BloodGroup(models.Model):
    group_name = models.CharField(
        max_length=5, unique=True, verbose_name="Խմբի անվանում"
    )

    def __str__(self):
        return self.group_name


class Condition(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Հիվանդության անվանում"
    )

    class Meta:
        verbose_name = "Հիվանդություն"
        verbose_name_plural = "Հիվանդություններ"

    def __str__(self):
        return self.name


class Medication(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Դեղամիջոցի անվանում"
    )

    class Meta:
        verbose_name = "Դեղամիջոց"
        verbose_name_plural = "Դեղամիջոցներ"

    def __str__(self):
        return self.name


class Surgery(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Վիրահատության անվանում"
    )

    class Meta:
        verbose_name = "Վիրահատություն"
        verbose_name_plural = "Վիրահատություններ"

    def __str__(self):
        return self.name


class Allergy(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Ալերգիայի անվանում"
    )

    class Meta:
        verbose_name = "Ալերգիա"
        verbose_name_plural = "Ալերգիաներ"

    def __str__(self):
        return self.name

def profile_pic_path(instance, filename):
    """
    Նկարները կվերբեռնվեն MEDIA_ROOT/profile_pics/<user_email>/<filename> ճանապարհով։
    instance-ը CustomUser օբյեկտն է։
    """
    # Քանի որ instance-ն արդեն CustomUser օբյեկտն է, մենք պարզապես դիմում ենք նրա email դաշտին
    folder_name = instance.email if instance.email else str(instance.id)
    # Ես փոխել եմ "face" թղթապանակի անունը "profile_pics"-ի՝ ավելի տրամաբանական լինելու համար
    return os.path.join('face', folder_name, filename)
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
        upload_to=profile_pic_path, # Նախկին "profile_pics/"-ի փոխարեն նշում ենք մեր ֆունկցիան
        null=True, 
        blank=True, 
        verbose_name="Պրոֆիլի նկար"
    )
    
    public_profile_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="Հանրային ID (QR)"
    )

    def __str__(self):
        return self.get_full_name() or self.username


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
        full_name = self.user.get_full_name()
        return (
            f"Բժիշկ՝ {full_name}"
            if full_name
            else f"Doctor Profile ({self.user.username})"
        )


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
        return f"Պացիենտ՝ {self.user.get_full_name()}"


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


import os  # Համոզվիր, որ os-ը import արված է ֆայլի սկզբում

# ... քո մյուս import-ները և մոդելները


# ԱՎԵԼԱՑՐՈՒ ԱՅՍ ՖՈՒՆԿՑԻԱՆ
def user_directory_path(instance, filename):
    """
    Ֆայլերը կվերբեռնվեն MEDIA_ROOT/face_recognition_images/<user_email>/<filename> ճանապարհով
    instance - UserFaceImage մոդելի օբյեկտն է, որը պահպանվում է
    filename - ֆայլի օրիգինալ անվանումն է
    """
    user_email = instance.user.email
    # os.path.join-ը ստեղծում է ճիշտ ճանապարհ՝ անկախ օպերացիոն համակարգից
    return os.path.join("face", user_email, filename)


# ...


# Այժմ փոփոխիր UserFaceImage մոդելը
class UserFaceImage(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="face_images",
        verbose_name="Օգտատեր",
    )
    # Այստեղ upload_to-ին տալիս ենք մեր ստեղծած ֆունկցիան
    image = models.ImageField(upload_to=user_directory_path, verbose_name="Նկար")
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Վերբեռնման ամսաթիվ"
    )

    class Meta:
        verbose_name = "Դեմքի նկար"
        verbose_name_plural = "Դեմքի նկարներ"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Նկար {self.user.username}-ի համար, վերբեռնված՝ {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
