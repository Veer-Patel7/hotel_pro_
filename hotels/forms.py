# forms.py
from django import forms
from .models import Hotel, Room, RoomCategory, HotelImage
import datetime
import re

class HotelBasicInfoForm(forms.ModelForm):

    current_year = datetime.date.today().year
    YEAR_CHOICES = [(year, year) for year in range(current_year, 1950, -1)]

    year_built = forms.ChoiceField(choices=YEAR_CHOICES)

    class Meta:
        model = Hotel
        fields = [
            "property_name",
            "star_rating",
            "year_built",
            "mobile_number",
            "email",
        ]

        widgets = {
            "property_name": forms.TextInput(attrs={"class": "form-control"}),
            "star_rating": forms.Select(attrs={"class": "form-control"}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        
INDIAN_STATES = [
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Bihar", "Bihar"),
    ("Delhi", "Delhi"),
    ("Gujarat", "Gujarat"),
    ("Karnataka", "Karnataka"),
    ("Maharashtra", "Maharashtra"),
    ("Rajasthan", "Rajasthan"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("West Bengal", "West Bengal"),
]


class HotelLocationForm(forms.ModelForm):

    state = forms.ChoiceField(choices=INDIAN_STATES)

    class Meta:
        model = Hotel
        fields = [
            "use_current_location",
            "latitude",
            "longitude",
            "house_no",
            "area",
            "pincode",
            "country",
            "state",
            "city",
            "terms_accepted",
        ]

        widgets = {
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "house_no": forms.TextInput(attrs={"class": "form-control"}),
            "area": forms.TextInput(attrs={"class": "form-control"}),
            "pincode": forms.TextInput(attrs={"class": "form-control", "maxlength": "6"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            # "country": forms.Select(attrs={"class": "form-control"}),
        }
        
    def clean_pincode(self):
        pincode = self.cleaned_data.get("pincode")

        if not re.match(r"^[1-9][0-9]{5}$", pincode):
            raise forms.ValidationError("Enter valid 6-digit Indian pincode.")

        return pincode
    
class HotelAmenitiesForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["amenities"]
        widgets = {
            "amenities": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Example: Free WiFi, Swimming Pool, Parking, Gym..."
            })
        }



class RoomCategoryForm(forms.ModelForm):
    class Meta:
        model = RoomCategory
        exclude = ["hotel", "is_active"]

        widgets = {
            "extra_bed_allowed": forms.RadioSelect(
                choices=[(True, "Yes"), (False, "No")]
            )
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["category", "room_number", "status"]

    def __init__(self, *args, **kwargs):
        hotel = kwargs.pop("hotel", None)
        super().__init__(*args, **kwargs)

        if hotel:
            self.fields["category"].queryset = RoomCategory.objects.filter(hotel=hotel)
# # forms.py
# from django import forms
# from .models import Room

# class RoomForm(forms.ModelForm):
#     class Meta:
#         model = Room
#         fields = [
#             'room_type',
#             'room_number',
#             'room_size',
#             'max_guest',
#             'price_per_night',
#             'status'
#         ]

#         widgets = {
#             'room_type': forms.TextInput(attrs={'class': 'form-control'}),
#             'room_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'room_size': forms.NumberInput(attrs={'class': 'form-control'}),
#             'max_guest': forms.NumberInput(attrs={'class': 'form-control'}),
#             'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
#             'status': forms.Select(choices=[
#                 ('available', 'Available'),
#                 ('booked', 'Booked'),
#                 ('maintenance', 'Maintenance')
#             ], attrs={'class': 'form-control'}),
#         }
class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ["image"]