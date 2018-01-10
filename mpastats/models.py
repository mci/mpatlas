from django.db import models
# from django.contrib.gis.db import models
# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
# from django.db import connection, transaction
from django.core.exceptions import ValidationError

# Create your models here.

class Coverage(models.Model):
    global_marinearea = models.FloatField(null=True, blank=True)
    global_mpa = models.FloatField(null=True, blank=True)
    global_strong = models.FloatField(null=True, blank=True)
    global_notake = models.FloatField(null=True, blank=True)
    global_unimplemented = models.FloatField(null=True, blank=True)
    global_proposed = models.FloatField(null=True, blank=True)

    eez_marinearea = models.FloatField(null=True, blank=True)
    eez_mpa = models.FloatField(null=True, blank=True)
    eez_strong = models.FloatField(null=True, blank=True)
    eez_notake = models.FloatField(null=True, blank=True)
    eez_unimplemented = models.FloatField(null=True, blank=True)
    eez_proposed = models.FloatField(null=True, blank=True)

    abnj_marinearea = models.FloatField(null=True, blank=True)
    abnj_mpa = models.FloatField(null=True, blank=True)
    abnj_strong = models.FloatField(null=True, blank=True)
    abnj_notake = models.FloatField(null=True, blank=True)
    abnj_unimplemented = models.FloatField(null=True, blank=True)
    abnj_proposed = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if Coverage.objects.exists() and not self.pk:
        # check for self.pk incase this is update of existing instance
            raise ValidationError('There is can be only one mpastats.Coverage instance')
        return super(Coverage, self).save(*args, **kwargs)