# app/plants/forms.py

from django                 import forms
from django_quill.forms     import QuillFormField
from django.core.validators import URLValidator

PEST_TYPE_CHOICES = (
	("tbd",     "tbd"),
	("Insect",  "Insect"),
	("Mollusk", "Mollusk"),
	("Disease", "Disease"),
	("Weed",    "Weed"),
)

class PestAddUpdateForm(forms.Form):
	pest_name = forms.CharField(
		label="Pest Name", 
		max_length=255,
		)
	# Attributes
	pest_type = forms.ChoiceField(
		label="Pest Type",
		initial='tbd',
		choices = PEST_TYPE_CHOICES,
		required=False,
		)
	#
	description = QuillFormField(
		label="Description",
		initial="tbd",
		required=False,
	)
	#
	management = QuillFormField(
		label="Management",
		initial="tbd",
		required=False,
	)
	# pest images
	image_1   = forms.ImageField(
		required=False,
		widget=forms.FileInput()
	)
	caption_1 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
	)
	image_2   = forms.ImageField(
		required=False,
		widget=forms.FileInput()
	)
	caption_2 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
	)
	image_3 = forms.ImageField(
		required=False,
		widget=forms.FileInput()
	)
	caption_3 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
	)
	image_4 = forms.ImageField(
		required=False,
		widget=forms.FileInput()
	)
	caption_4 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False,
	)
	# UC IPM URL
	pest_url = forms.URLField(
		label="UC IPM URL",
		validators=[URLValidator()],
		widget=forms.TextInput(attrs={'placeholder': 'https://example.com'})
	)