# /plants/forms.py

from django import forms 
from django_quill.forms import QuillFormField
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

TYPE_CHOICES = (
	("tbd",         "tbd"),
	("Annual",      "Annual"),
	("Grass",       "Grass"),
	("Groundcover", "Groundcover"),
	("Perennial",   "Perennial"),
	("Shrub",       "Shrub"),
	("Succulent",   "Succulent"),
	("Tree",        "Tree"),
	("Vegetable",   "Vegetable"),
	("Vine",        "Vine"),
)
BLOOM_COLOR_CHOICES = ( 
	('tbd',       'tbd'),
	('white',     'white'),
	('yellow',    'yellow'),
	('red',       'red'), 
	('pink',      'pink'),
	('pale pink', 'pale pink'),
	('purple',    'purple'),
	('green',     'green'), 
	('blue',      'blue'), 
	('orange',    'orange'), 
) 
BLOOM_SEASON_CHOICES = (
	("tbd",    "tbd"),
	("Spring", "Spring"), 
	("Summer", "Summer"), 
	("Fall",   "Fall"),
	("Winter", "Winter"),
	("None",   "None"),
)
POLLINATORS_CHOICES = (
	("tbd",          "tbd"),
	("Bees",         "Bees"),
	("Butterfiles",  "Butterfiles"),
	("Hummingbirds", "Hummingbirds"),
	("None",         "None"),
)
SUN_EXPOSURE_CHOICES = (
	("tbd",           "tbd"),
	("Full Sun",      "Full Sun"),
	("Partial Sun",   "Partial Sun"),
	("Partial Shade", "Partial Shade"),
	("Full Shade",    "Full Shade"),
)
WATER_RQMTS_CHOICES = (
	("tbd",       "tbd"),
	("Very Low",  "Very Low"),
	("Low",       "Low"),
	("Medium",    "Medium"),
	("High",      "High"),
	("Very High", "Very High"),
)
SOIL_TYPE_CHOICES = (
	("tbd",    "tbd"),
	("Sandy",  "Sandy"),
	("loamy",  "Loamy"),
	("Clay",   "Clay"),
)
PH_CHOICES = (
	("tbd", "tbd"),
	("5.5", "5.5"),
	("5.6", "5.6"),
	("5.7", "5.7"),
	("5.8", "5.8"),
	("5.9", "5.9"),
	("6.0", "6.0"),
	("6.1", "6.1"),
	("6.2", "6.2"),
	("6.3", "6.3"),
	("6.4", "6.4"),
	("6.5", "6.5"),
	("6.6", "6.6"),
	("6.7", "6.7"),
	("6.8", "6.8"),
	("6.9", "6.9"),
	("7.0", "7.0"),
	("7.1", "7.1"),
	("7.2", "7.2"),
	("7.3", "7.3"),
	("7.4", "7.4"),
	("7.5", "7.5"),
	("7.6", "7.6"),
	("7.7", "7.7"),
	("7.8", "7.8"),
	("7.9", "7.9"),
	("8.0", "8.0"),
)
UCD_ALL_STAR_CHOICES = (
	("tbd", "tbd"),
	("Yes", "Yes"),
	("No",  "No"),
)
CA_NATIVE_CHOICES = (
	("tbd", "tbd"),
	("Yes", "Yes"),
	("No",  "No"),
)
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

class UserSignupForm(forms.Form):
	username = forms.CharField(
		label="username", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	password = forms.CharField(
		label="password", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}),
		)
	email = forms.EmailField(
		label="email", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	first_name = forms.CharField(
		label="first_name", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	last_name = forms.CharField(
		label="last_name", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	
class UserLoginForm(forms.Form):
	username = forms.CharField(
		label="username", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	password = forms.CharField(
		label="password", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}),
		)
	
class GardenAddUpdateForm(forms.Form):
	name = forms.CharField(
		label="Garden Name", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	city = forms.CharField(
		label="City", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	state = forms.CharField(
		label="State", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
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
	# garden images
	image_1   = forms.ImageField(required=False)
	caption_1 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_2   = forms.ImageField(required=False)
	caption_2 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_3   = forms.ImageField(required=False)
	caption_3 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_4   = forms.ImageField(required=False)
	caption_4 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_5   = forms.ImageField(required=False)
	caption_5 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_6   = forms.ImageField(required=False)
	caption_6 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_7   = forms.ImageField(required=False)
	caption_7 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_8   = forms.ImageField(required=False)
	caption_8 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	
class MyPlantAddUpdateForm(forms.Form):
	date_planted = forms.DateField(
		widget=DatePickerInput(),
		label="Date Planted",
		required=False,
	)
	location = forms.CharField(
		label='Location', 
		max_length=64, 
		required=False,
		)
	sun_exposure = forms.MultipleChoiceField(
		label='Sun Exposure',
		initial='tbd',
		choices = SUN_EXPOSURE_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=False,
		)
	pH = forms.ChoiceField(
		label="pH",
		choices = PH_CHOICES, 
		required=False,
		)
	soil_type = forms.MultipleChoiceField(
		label="Soil Type",
		initial='tbd',
		choices = SOIL_TYPE_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=False,
		)

class MyPlantCommentForm(forms.Form):
	subject = forms.CharField(
		label='Subject', 
		max_length=64, 
		required=False,
		)
	comment = QuillFormField(
		label="Comment",
		required=False,
	)

class PlantAddUpdateForm(forms.Form):
	commonName = forms.CharField(
		label="Common Name", 
		max_length=255,
		)
	# Attributes
	type_x = forms.ChoiceField(
		label="Type",
		initial='tbd',
		choices = TYPE_CHOICES,
		required=False,
		)
	bloom_color = forms.MultipleChoiceField(
		label="Bloom Color",
		initial='tbd',
		choices = BLOOM_COLOR_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=False,
		)
	bloom_season = forms.MultipleChoiceField(
		label="Bloom Season",
		initial='tbd',
		choices = BLOOM_SEASON_CHOICES,
		widget=forms.CheckboxSelectMultiple, 
		required=False,
		)
	height_feet = forms.IntegerField(
		label="Height (ft)",
		initial="0", 
		required=False,
		)
	height_inch = forms.IntegerField(
		label="Height (in)",
		initial="0", 
		required=False,
		)
	width_feet = forms.IntegerField(
		label="Width (ft)",
		initial="0", 
		required=False,
		)
	width_inch = forms.IntegerField(
		label="Width (in)",
		initial="0", 
		required=False,
		)
	pollinators = forms.MultipleChoiceField(
		label="Pollinators",
		initial='tbd',
		choices = POLLINATORS_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=False,
		)
	sun_exposure = forms.MultipleChoiceField(
		label="Sun Exposure",
		initial='tbd',
		choices = SUN_EXPOSURE_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=False,
		)
	water_rqmts = forms.ChoiceField(
		label="Water Requirements",
		choices = WATER_RQMTS_CHOICES, 
		required=False,
		)
	pH_min = forms.ChoiceField(
		label="pH (min)",
		choices = PH_CHOICES, 
		required=False,
		)
	pH_max = forms.ChoiceField(
		label="pH (max)",
		choices = PH_CHOICES, 
		required=False,
		)
	soil_type = forms.MultipleChoiceField(
		label="Soil Type",
		choices = SOIL_TYPE_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=False,
		)
	ucd_all_star = forms.ChoiceField(
		label="UCD All-Star",
		initial = 'tbd',
		choices = UCD_ALL_STAR_CHOICES, 
		widget=forms.RadioSelect,
		required=False,
		)
	ca_native = forms.ChoiceField(
		label="California Native",
		initial = 'tbd',
		choices = CA_NATIVE_CHOICES, 
		widget=forms.RadioSelect,
		required=False,
		)
	usda_zone_min = forms.ChoiceField(
		label="USDA Zone (min)",
		choices = USDA_ZONE_CHOICES, 
		required=False,
		)
	usda_zone_max = forms.ChoiceField(
		label="USDA Zone (max)",
		choices = USDA_ZONE_CHOICES, 
		required=False,
		)
	sunset_zones = forms.CharField(
		label='Sunset Zones',
		initial="tbd", 
		max_length=32, 
		required=False
		)
	#
	description = QuillFormField(
		label="Description",
		required=False,
	)
	pruning = QuillFormField(
		label="Pruning Considerations",
		required=False,
	)
	fertilization = QuillFormField(
		label="Fertilization Considerations",
		required=False,
	)
	# plant taxonomy
	kingdom = forms.CharField(
		label="Kingdom",
		initial="tbd",
		max_length=255, 
		required=False,
		)
	subkingdom = forms.CharField(
		label="Subkingdom",
		initial="tbd",
		max_length=255, 
		required=False,
		)
	superdivision = forms.CharField(
		label="Superdivision", 
		initial="tbd",
		max_length=255, 
		required=False,
		)
	division = forms.CharField(
		label="Division", 
		initial="tbd",
		max_length=255, 
		required=False,
		)
	class_x = forms.CharField(
		label="Class", 
		initial="tbd",
		max_length=255, 
		required=False,
		)
	subclass = forms.CharField(
		label="Subclass", 
		initial="tbd",
		max_length=255, 
		required=False,
		)
	order = forms.CharField(
		label="Order",
		initial="tbd", 
		max_length=255, 
		required=False
		)
	family = forms.CharField(
		label="Family",
		initial="tbd", 
		max_length=255, 
		required=False
		)
	genus = forms.CharField(
		label="Genus",
		initial="tbd", 
		max_length=255, 
		required=False
		)
	species = forms.CharField(
		label="Species",
		initial="tbd", 
		max_length=255, 
		required=False
		)
	variety = forms.CharField(
		label="Variety",
		initial="tbd", 
		max_length=255, 
		required=False
		)
	phonetic_spelling = forms.CharField(
		label="Phonetic Spelling",
		initial="tbd", 
		max_length=32, 
		required=False
		)
	pronunciation = forms.URLField(
		label="Pronunciation URL",
		initial="https://temp.com", 
		max_length=255, 
		required=False
	)
	# plant images
	image_1   = forms.ImageField(required=False)
	caption_1 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_2   = forms.ImageField(required=False)
	caption_2 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_3 = forms.ImageField(required=False)
	caption_3 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False
		)
	image_4 = forms.ImageField(required=False)
	caption_4 = forms.CharField(
		label="Caption",
		initial="tbd", 
		max_length=64, 
		required=False,
		)
	creator_notes  = QuillFormField(
		label="Creator Notes:",
		required=False,
	)
	
class PlantCommentForm(forms.Form):
	subject = forms.CharField(
		label='Subject', 
		max_length=64, 
		required=False,
		)
	comment = QuillFormField(
		label="Comment",
		required=False,
	)