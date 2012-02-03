from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

TITLE_CHOICES = (
    ('', ''),
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Ms','Ms'),
    ('Miss','Miss'),
    ('Dr', 'Dr'),
)

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    title = models.CharField(max_length=20, default='', choices=TITLE_CHOICES)
    affiliation = models.CharField('organization', max_length=300)
    country = models.CharField(max_length=300)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
