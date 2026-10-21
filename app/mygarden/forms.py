# /app/mygarden/forms.py

from django import forms 
from django_quill.forms       import QuillFormField

USDA_ZONE_CHOICES = (
	("tbd",               "tbd"),
	("1a (-60F to -55F)", "1a (-60F to -55F)"),
	("1b (-55F to -50F)", "1b (-55F to -50F)"),
	("2a (-50F to -45F)", "2a (-50F to -45F)"),
	("2b (-45F to -40F)", "2b (-45F to -40F)"),
	("3a (-40F to -35F)", "3a (-40F to -35F)"),
	("3b (-35F to -30F)", "3b (-35F to -30F)"),
	("4a (-30F to -25F)", "4a (-30F to -25F)"),
	("4b (-25F to -20F)", "4b (-25F to -20F)"), 
	("5a (-20F to -15F)", "5a (-20F to -15F)"),
	("5b (-15F to -10F)", "5b (-15F to -10F)"), 
	("6a (-10F to -5F)",  "6a (-10F to -5F)"), 
	("6b (-5F to 0F)",    "6b (-5F to 0F)"), 
	("7a (0F to 5F)",     "7a (0F to 5F)"), 
	("7b (5F to 10F)",    "7b (5F to 10F)"), 
	("8a (10F to 15F)",   "8a (10F to 15F)"), 
    ("8b (15F to 20F)",   "8b (15F to 20F)"), 
	("9a (20F to 25F)",   "9a (20F to 25F)"),
	("9b (25F to 30F)",   "9b (25F to 30F)"), 
	("10a (30F to 35F)",  "10a (30F to 35F)"), 
	("10b (35F to 40F)",  "10b (35F to 40F)"),
	("11a (40F to 45F)",  "11a (40F to 45F)"), 
	("11b (45F to 50F)",  "11b (45F to 50F)"),
	("12a (50F to 55F)",  "12a (50F to 55F)"), 
	("12b (55F to 60F)",  "12b (55F to 60F)"),
	("13a (60F to 65F)",  "13a (60F to 65F)"), 
	("13b (65F to 70F)",  "13b (65F to 70F)"),
)

class GardenAddUpdateForm(forms.Form):
	name = forms.CharField(
		label="Garden Name", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'bnd-input bnd-border'}),
		)
	city = forms.CharField(
		label="City", 
		max_length=64, 
		required=False,
		widget=forms.TextInput(attrs={'class': 'bnd-input bnd-border'}),
		)
	state = forms.CharField(
		label="State", 
		max_length=64, 
		required=False,
		widget=forms.TextInput(attrs={'class': 'bnd-input bnd-border'}),
		)
	usda_zone = forms.ChoiceField(
		label="USDA Zone",
		choices = USDA_ZONE_CHOICES, 
		required=False,
		)
	sunset_zone = forms.CharField(
		label='Sunset Zone',
		initial="tbd", 
		max_length=32, 
		required=False
		)
	description = QuillFormField(
        label="Description",
        required=False,
        )
	# garden images
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
	image_3   = forms.ImageField(
		required=False,
		widget=forms.FileInput()
		)
	caption_3 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_4   = forms.ImageField(
		required=False,
		widget=forms.FileInput()
		)
	caption_4 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_5   = forms.ImageField(
		required=False,
		widget=forms.FileInput()
		)
	caption_5 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_6   = forms.ImageField(
		required=False,
		widget=forms.FileInput()
		)
	caption_6 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_7   = forms.ImageField(
		required=False,
		widget=forms.FileInput()
		)
	caption_7 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_8   = forms.ImageField(
		required=False,
		widget=forms.FileInput()
		)
	caption_8 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)