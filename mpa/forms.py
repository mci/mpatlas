#from django import forms
from django.forms import ModelForm
from django import forms
from mpa.models import Mpa
# from tinymce.widgets import TinyMCE
from ckeditor.fields import RichTextField
from django.contrib.admin.widgets import AdminDateWidget

# Create the form class.
class MpaForm(ModelForm):
    edit_reference = forms.CharField(widget=forms.Textarea, required=False, label="Data Reference for your edits", help_text="Please list a source reference for any changes you have made to this MPA record.  This can be a published report, online database, government office, or personal communication.")
    edit_comment = forms.CharField(widget=forms.Textarea, max_length=1000, required=False, label="Additional comment for this edit", help_text="Please describe your reasoning for this edit so we can keep track of how our database is improving.")
    class Meta:
        model = Mpa
        exclude = ('geom',)
        widgets = {
            'summary': RichTextField(),
            'verified_date': AdminDateWidget(),
            'implementation_date': AdminDateWidget()
        }

class MpaGeomForm(ModelForm):
    boundarygeo = forms.CharField(widget=forms.Textarea, required=False, label="MPA Site Boundaries", help_text="Please enter a geojson geometry object here as a polygon or multipolygon.")
    boundaryfile = forms.FileField(required=False, label="MPA Site Boundaries geojson file")
    class Meta:
        model = Mpa
        fields = []
        # exclude = ()
        widgets = {}
# Creating a form to submit a new rsvp response
#newform = TegnerForm()

# Creating a form to change an existing Rsvp response.
#tegnerobject = TegnerProposal.objects.get(pk=1)
#changeform = TegnerForm(instance=tegnerobject)
