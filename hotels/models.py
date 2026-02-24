from django.db import models
from accounts.models import User

class Hotel(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    hotel_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100,null=True, blank=True)

    id_proof1 = models.FileField(upload_to="hotel_docs/",null=True, blank=True)
    id_proof2 = models.FileField(upload_to="hotel_docs/",null=True, blank=True)

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("blocked", "Blocked"),
        ("rejected", "Rejected"),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    reject_reason = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.hotel_name


# class Hotel(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     hotel_name = models.CharField(max_length=100)
#     property_type = models.CharField(max_length=50)
#     star_rating = models.IntegerField()
#     description = models.TextField()
#     price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    
#     country = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     address = models.TextField()
#     pincode = models.CharField(max_length=10)

#     is_approved = models.BooleanField(default=False)
#     is_blocked = models.BooleanField(default=False)

#     def __str__(self):
#         return self.hotel_name

from django.db import models

class RoomCategory(models.Model):
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE, related_name="room_categories")

    ROOM_TYPES = (
        ("standard", "Standard"),
        ("deluxe", "Deluxe"),
        ("suite", "Suite"),
    )

    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    room_size = models.PositiveIntegerField(help_text="Size in square feet")
    max_guest = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.hotel_name} - {self.get_room_type_display()}"
    
class Room(models.Model):
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE, related_name="rooms")
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name="rooms")

    room_number = models.CharField(max_length=10, unique=True)

    STATUS_CHOICES = (
        ("available", "Available"),
        ("maintenance", "Maintenance"),
        ("blocked", "Blocked"),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    def __str__(self):
        return f"{self.hotel.hotel_name} - Room {self.room_number}"
    
class RoomAvailability(models.Model):
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name="availability")
    date = models.DateField()
    booked_rooms = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("category", "date")

    @property
    def available_rooms(self):
        return self.category.total_rooms - self.booked_rooms

    def __str__(self):
        return f"{self.category} - {self.date}"
# class Room(models.Model):
#     hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
#     room_type = models.CharField(max_length=20)
#     room_number = models.CharField(max_length=10)
#     room_size = models.IntegerField()
#     max_guest = models.IntegerField()
#     price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

#     status = models.CharField(max_length=20, default="available")

#     def __str__(self):
#         return f"{self.hotel.hotel_name} - {self.room_number}"
