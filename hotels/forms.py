# forms.py

from django import forms
from .models import Room, RoomCategory

class RoomCategoryForm(forms.ModelForm):
    class Meta:
        model = RoomCategory
        exclude = ("hotel",)


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