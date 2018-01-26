#from django import forms
from django.forms import Form, ModelForm
from django import forms
from campaign.models import Campaign
# from tinymce.widgets import TinyMCE
from ckeditor.fields import RichTextField
from django.contrib.admin.widgets import AdminDateWidget

class CampaignGeomForm(ModelForm):
    boundarygeo = forms.CharField(widget=forms.Textarea, required=False, label="Campaign Point or Area of Interest", help_text="Please enter a geojson geometry object here as a point, polygon or multipolygon.")
    boundaryfile = forms.FileField(required=False, label="Campaign Point or Area geojson file")
    class Meta:
        model = Campaign
        fields = []
        # exclude = ()
        widgets = {}

# Creating a form to submit a new rsvp response
#newform = TegnerForm()

# Creating a form to change an existing Rsvp response.
#tegnerobject = TegnerProposal.objects.get(pk=1)
#changeform = TegnerForm(instance=tegnerobject)
