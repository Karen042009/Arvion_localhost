# your_app/migrations/0003_populate_blood_groups.py

from django.db import migrations

# Արյան խմբերի ցուցակը
BLOOD_GROUPS = [
    "O(I) Rh+",
    "O(I) Rh-",
    "A(II) Rh+",
    "A(II) Rh-",
    "B(III) Rh+",
    "B(III) Rh-",
    "AB(IV) Rh+",
    "AB(IV) Rh-",
]

def populate_blood_groups(apps, schema_editor):
    """
    Ավելացնում է արյան հիմնական խմբերը BloodGroup մոդելում։
    """
    BloodGroup = apps.get_model('main', 'BloodGroup') # Փոխարինիր your_app-ը
    for group_name in BLOOD_GROUPS:
        # get_or_create-ը կստեղծի խումբը միայն այն դեպքում, եթե այն դեռ գոյություն չունի
        BloodGroup.objects.get_or_create(group_name=group_name)

def remove_blood_groups(apps, schema_editor):
    """
    (Optional) Թույլ է տալիս ջնջել այս խմբերը, եթե միգրացիան հետ ենք տալիս։
    """
    BloodGroup = apps.get_model('main', 'BloodGroup') # Փոխարինիր your_app-ը
    BloodGroup.objects.filter(group_name__in=BLOOD_GROUPS).delete()


class Migration(migrations.Migration):

    dependencies = [
        # Այստեղ պետք է լինի ձեր նախորդ միգրացիայի ֆայլի անունը, օրինակ՝
        ('main', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(populate_blood_groups, remove_blood_groups),
    ]