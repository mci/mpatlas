from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.contrib import auth

TITLE_CHOICES = (
    ('--', ''),
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Ms','Ms'),
    ('Miss','Miss'),
    ('Dr', 'Dr'),
)

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Other fields here
    title = models.CharField(max_length=200, default='', choices=TITLE_CHOICES)
    affiliation = models.CharField('organization', max_length=300, blank=True)
    country = CountryField()
    
    def __unicode__(self):
        return '%s - %s %s' % (self.user.username, self.user.first_name, self.user.last_name)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
