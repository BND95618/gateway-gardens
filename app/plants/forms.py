# /plants/forms.py

from django import forms 
from django_quill.forms       import QuillFormField
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
import datetime
from django.core.validators   import URLValidator

TYPE_CHOICES = (
	("tbd",         "tbd"),
	("Annual",      "Annual"),
	("Fern",        "Fern"),
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
	('none',      'none'),
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
	("Butterflies",  "Butterflies"),
	("Hummingbirds", "Hummingbirds"),
	("None",         "None"),
)
CA_NATIVE_CHOICES = (
	("tbd", "tbd"),
	("Yes", "Yes"),
	("No",  "No"),
)
UCD_ALL_STAR_CHOICES = (
	("tbd", "tbd"),
	("Yes", "Yes"),
	("No",  "No"),
)
DAVIS_TREE_CHOICES = (
	("tbd", "tbd"),
	("Yes", "Yes"),
	("No",  "No"),
)
SUNSET_Z14_CHOICES = (
	("tbd", "tbd"),
	("Yes", "Yes"),
	("No",  "No"),
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
PH_CHOICES = (
	("tbd", "tbd"),
	("5.0", "5.0"),
	("5.1", "5.1"),
	("5.2", "5.2"),
	("5.3", "5.3"),
	("5.4", "5.4"),
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
SOIL_TYPE_CHOICES = (
	("tbd",    "tbd"),
	("Sandy",  "Sandy"),
	("Loamy",  "Loamy"),
	("Clay",   "Clay"),
)
HEAT_TOLERANCE_CHOICES = (
	("tbd",       "tbd"),
	("Poor",      "Poor"),
	("Fair",      "Fair"),
	("Good",      "Good"),
	("Excellent", "Excellent"),
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
HAPPINESS_CHOICES = (
	("tbd",          "tbd"),
	("Very Happy",   "Very Happy"),
	("Happy",        "Happy"),
	("Neutral",      "Neutral"),
	("Unhappy",      "Unhappy"),
	("Very Unhappy", "Very Unhappy"),
)
STATUS_CHOICES = (
	("Development", "Development"),
	("Review",      "Review"),
	("Published",   "Published"),
	("Archived",    "Archived"),
)
#
TODO_ACTION_CHOICES = (
	("Fertilize", "Fertilize"),
	("Harvest",   "Harvest"),
	("Mow",       "Mow"),
	("Plant",     "Plant"),
	("Prune",     "Prune"),
	("Spray",     "Spray"),
	("Other",     "Other"),
)
TODO_REPEAT_CHOICES = (
	("Daily",     "Daily"),
	("Weekly",    "Weekly"),
	("Bi-Weekly", "Bi-Weekly"),
	("Monthly",   "Monthly"),
	("Yearly",    "Yearly"),
	("None",      "None"),
)
MONTH_CHOICES = (
	("tbd",  "tbd"),
	("Jan",  "Jan"),
	("Feb",  "Feb"),
	("Mar",  "Mar"),
	("Apr",  "Apr"),
	("May",  "May"),
	("Jun",  "Jun"),
	("Jul",  "Jul"),
	("Aug",  "Aug"),
	("Sep",  "Sep"),
	("Oct",  "Oct"),
	("Nov",  "Nov"),
	("Dec",  "Dec"),
	("None", "None")
)
COLUMN_CHOICES = (
	("Common Name",     "Common Name"),
	("Genus/Species",   "Genus/Species"),
	("Variety",         "Variety"),
	# Plant Characteristics
	("Type",            "Type"),
	("Height",          "Height"),
	("Width", 		    "Width"),
	("Bloom Color",     "Bloom Color"),
	("Bloom Season",    "Bloom Season"),
	("Bloom Range",     "Bloom Range"),
	("Pollinators",     "Pollinators"),
	("CA Native",       "CA Native"),
	("UCD All-Star",    "UCD All-Star"),
	("Davis Trees",     "Davis Trees"),
	("Sunset Z14",      "Sunset Z14"),
	# Plant Requirements
	("Sun Exposure",    "Sun Exposure"),
	("Water Rqmts",     "Water Rqmts"),
	("Soil Type",       "Soil Type"),
	("pH Range",        "pH Range"),
	("Heat Tolerance",  "Heat Tolerance"),
	("USDA Zones",      "USDA Zones"),
	("Sunset Zones",    "Sunset Zones"),
	# Admin
	("Status",          "Status"),
)
MY_COLUMN_CHOICES = (
	("Common Name",     "Common Name"),
	("Genus/Species",   "Genus/Species"),
	("Variety",         "Variety"),
	# Plant Characteristics
	("Type",            "Type"),
	("Height",          "Height"),
	("Width", 		    "Width"),
	("Bloom Color",     "Bloom Color"),
	("Bloom Season",    "Bloom Season"),
	("Bloom Range",     "Bloom Range"),
	("Pollinators",     "Pollinators"),
	("CA Native",       "CA Native"),
	("UCD All-Star",    "UCD All-Star"),
	("Davis Trees",     "Davis Trees"),
	("Sunset Z14",      "Sunset Z14"),
	# Plant Requirements
	("Sun Exposure",    "Sun Exposure"),
	("Water Rqmts",     "Water Rqmts"),
	("Soil Type",       "Soil Type"),
	("pH Range",        "pH Range"),
	("Heat Tolerance",  "Heat Tolerance"),
	("USDA Zones",      "USDA Zones"),
	("Sunset Zones",    "Sunset Zones"), 
	# Garden Environment
	("My Location",        "My Location"),
	("My Sun Exposure",    "My Sun Exposure"),
	("My Water Level",     "My Water Level"),
	("My Soil Type",       "My Soil Type"),
	("My pH",              "My pH"),
	("My Bloom Color",     "My Bloom Color"),
	("My Bloom Range",     "My Bloom Range"),
	#
	("Happy?",          "Happy?"),
)
PEST_TYPE_CHOICES = (
	("tbd",     "tbd"),
	("Insect",  "Insect"),
	("Disease", "Disease"),
	("Weed",    "Weed"),
)

class UserSignupForm(forms.Form):
	signup_username = forms.CharField(
		label="Username", 
		max_length=64,
		widget=forms.TextInput(attrs={'class' : 'w3-input w3-border'}),
		)
	signup_password = forms.CharField(
		label="Password", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class' : 'w3-input w3-border'}),
		)
	signup_password_2 = forms.CharField(
		label="Password (reconfirm)", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class' : 'w3-input w3-border'}),
		)
	email = forms.CharField(
		label="e-mail address", 
		max_length=64,
		widget=forms.TextInput(attrs={'class'        : 'w3-input w3-border', 
								      'autocomplete' : 'email'}),
		)
	first_name = forms.CharField(
		label="First Name", 
		max_length=64,
		widget=forms.TextInput(attrs={'class'        : 'w3-input w3-border', 
								      'autocomplete' : 'given-name'}),
		)
	last_name = forms.CharField(
		label="Last Name", 
		max_length=64,
		widget=forms.TextInput(attrs={'class'        : 'w3-input w3-border', 
								      'autocomplete' : 'family-name'}),
		)
	
class UserLoginForm(forms.Form):
	username = forms.CharField(
		label="Username", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	password = forms.CharField(
		label="Password", 
		max_length=64,
		widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}),
		)
	
class UserUpdateForm(forms.Form):
	new_username = forms.CharField(
		label="New Username", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	new_password = forms.CharField(
		label="New Password", 
		max_length=64,
		required=False,
		widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}),
		)
	new_password_2 = forms.CharField(
		label="New Password (reconfirm)", 
		max_length=64,
		required=False,
		widget=forms.PasswordInput(attrs={'class': 'w3-input w3-border'}),
		)
	new_email = forms.CharField(
		label="New e-mail address", 
		max_length=64,
		widget=forms.TextInput(attrs={'class'        : 'w3-input w3-border', 
								      'autocomplete' : 'email'}),
		)
	new_first_name = forms.CharField(
		label="New First Name", 
		max_length=64,
		required=False,
		widget=forms.TextInput(attrs={'class'        : 'w3-input w3-border', 
								      'autocomplete' : 'given-name'}),
		)
	new_last_name = forms.CharField(
		label="New Last Name", 
		max_length=64,
		required=False,
		widget=forms.TextInput(attrs={'class'        : 'w3-input w3-border', 
								      'autocomplete' : 'family-name'}),
		)
	
class UserRecoveryForm(forms.Form):
	recovery_username = forms.CharField(
		label="Username", 
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	recovery_password = forms.CharField(
		label="Password", 
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
		required=False,
		widget=forms.TextInput(attrs={'class': 'w3-input w3-border'}),
		)
	state = forms.CharField(
		label="State", 
		max_length=64, 
		required=False,
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
		initial='tbd',      	
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
	water_level = forms.MultipleChoiceField(
		label='Water Level',
		initial='tbd',
		choices = WATER_RQMTS_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=False,
		)
	soil_type = forms.MultipleChoiceField(
		label="Soil Type",
		initial='tbd',
		choices = SOIL_TYPE_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=False,
		)
	pH = forms.ChoiceField(
		label="pH",
		choices = PH_CHOICES, 
		required=False,
		)
	bloom_color = forms.ChoiceField(
		label="Bloom Color",
		initial='tbd',
		choices = BLOOM_COLOR_CHOICES, 
		required=False,
		)
	bloom_start = forms.ChoiceField(
		label="Bloom Start",
		initial='tbd',
		choices = MONTH_CHOICES, 
		required=False,
		)
	bloom_end = forms.ChoiceField(
		label="Bloom End",
		initial='tbd',
		choices = MONTH_CHOICES, 
		required=False,
		)
	happiness = forms.ChoiceField(
		label="Happiness?",
		initial='tbd',
		choices = HAPPINESS_CHOICES, 
		required=False,
		)
	notes = QuillFormField(
		label="My Notes",
		initial="tbd",
		required=False,
		)

class MyPlantToDoForm(forms.Form):
	date = forms.DateField(
		label="Due Date",
		required=True,
		widget=forms.DateInput( 
			attrs=
				{'type'        : 'date',
	 			 'min'         : datetime.date.today(),
				},
				format='%Y-%m-%d'
			),
        )
	action = forms.ChoiceField(
		label="Action",
		initial=' ',
		choices = TODO_ACTION_CHOICES, 
		required=True,
		widget=forms.RadioSelect
		)
	repeat = forms.ChoiceField(
		label="Repeat",
		initial=' ',
		choices = TODO_REPEAT_CHOICES, 
		required=True,
		widget=forms.RadioSelect
		)
	details = forms.CharField(
		label="Details", 
		max_length=128, 
		required=True,
		widget=forms.TextInput(attrs={'class' : 'w3-input w3-border'}),
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

class MyColumnChooserForm(forms.Form):
	my_column_selection = forms.MultipleChoiceField(
		label="",
		initial='',
		choices = MY_COLUMN_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=True,
		)

class PlantAddUpdateForm(forms.Form):
	commonName = forms.CharField(
		label="Common Name", 
		max_length=255,
		)
	# Attributes
	type_x = forms.ChoiceField(
		label    = "Type",
		initial  = 'tbd',
		choices  = TYPE_CHOICES,
		required = False,
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
	bloom_start = forms.ChoiceField(
		label="Bloom Start",
		initial='tbd',
		choices = MONTH_CHOICES, 
		required=False,
		)
	bloom_end = forms.ChoiceField(
		label="Bloom End",
		initial='tbd',
		choices = MONTH_CHOICES, 
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
	ca_native = forms.ChoiceField(
		label="California Native",
		initial = 'tbd',
		choices = CA_NATIVE_CHOICES, 
		widget=forms.RadioSelect,
		required=False,
		)
	ucd_all_star = forms.ChoiceField(
		label="UCD All-Star",
		initial = 'tbd',
		choices = UCD_ALL_STAR_CHOICES, 
		widget=forms.RadioSelect,
		required=False,
		)	
	davis_trees = forms.ChoiceField(
		label="Davis Climate-Ready Trees",
		initial = 'tbd',
		choices = DAVIS_TREE_CHOICES, 
		widget=forms.RadioSelect,
		required=False,
		)
	sunset_z14 = forms.ChoiceField(
		label="Sunset Zone 14 Recommendation",
		initial = 'tbd',
		choices = SUNSET_Z14_CHOICES, 
		widget=forms.RadioSelect,
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
		initial='tbd',
		choices = SOIL_TYPE_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=False,
		)
	heat_tolerance = forms.ChoiceField(
		label="Heat Tolerance",
		choices = HEAT_TOLERANCE_CHOICES, 
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
		initial="tbd",
		required=False,
	)
	pruning = QuillFormField(
		label="Pruning Considerations",
		initial="tbd",
		required=False,
	)
	fertilization = QuillFormField(
		label="Fertilization Considerations",
		initial="tbd",
		required=False,
	)
	propagation = QuillFormField(
		label="Propagation Recommendations",
		initial="tbd",
		required=False,
	)
	pests_diseases = QuillFormField(
		label="Pest and Disease Considerations",
		initial="tbd",
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
		max_length=64, 
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
	status = forms.ChoiceField(
		label    = "Status",
		initial  = "Development",
		choices  = STATUS_CHOICES, 
		required = True,
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
	# UC IPM URL
	pest_url = forms.URLField(
		label="UC IPM URL",
		validators=[URLValidator()],
		widget=forms.TextInput(attrs={'placeholder': 'https://example.com'})
		)

class ColumnChooserForm(forms.Form):
	column_selection = forms.MultipleChoiceField(
		label="",
		initial='',
		choices = COLUMN_CHOICES, 
		widget=forms.CheckboxSelectMultiple,
		required=True,
		)
	