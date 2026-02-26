from django.db import models
from accounts.models import User
import datetime
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Hotel(models.Model):

    STAR_CHOICES = [
        (1, "1 Star"),
        (2, "2 Star"),
        (3, "3 Star"),
        (4, "4 Star"),
        (5, "5 Star"),
        (6, "6 Star"),
        (7, "7 Star"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # BASIC INFO
    property_name = models.CharField(max_length=200)
    star_rating = models.IntegerField(choices=STAR_CHOICES)
    year_built = models.IntegerField()

    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()

    # LOCATION INFO
    use_current_location = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    house_no = models.CharField(max_length=150, blank=True)
    area = models.CharField(max_length=150, blank=True)
    pincode = models.CharField(max_length=6, blank=True)

    country = models.CharField(max_length=100, default="India")
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    terms_accepted = models.BooleanField(default=False)

    # AMENITIES (NEW)
    amenities = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property_name


# class Hotel(models.Model):
#     owner = models.OneToOneField(User, on_delete=models.CASCADE)

#     hotel_name = models.CharField(max_length=100)
#     location = models.CharField(max_length=100,null=True, blank=True)

#     id_proof1 = models.FileField(upload_to="hotel_docs/",null=True, blank=True)
#     id_proof2 = models.FileField(upload_to="hotel_docs/",null=True, blank=True)

#     STATUS_CHOICES = (
#         ("pending", "Pending"),
#         ("approved", "Approved"),
#         ("blocked", "Blocked"),
#         ("rejected", "Rejected"),
#     )

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

#     reject_reason = models.TextField(null=True, blank=True)
    
#     def __str__(self):
#         return self.hotel_name




class RoomCategory(models.Model):
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE, related_name="room_categories")

    # ---------------- BASIC INFO ----------------
    room_name = models.CharField(max_length=100)

    ROOM_TYPE_CHOICES = [
        ("deluxe", "Deluxe"),
        ("standard", "Standard"),
        ("luxury", "Luxury"),
        ("master", "Master"),
        ("common", "Common"),
        ("family", "Family Room"),
        ("honeymoon", "For Honeymooners"),
        ("other", "Other"),
    ]

    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)

    BED_CHOICES = [
        ("single", "Single Bed"),
        ("double", "Double Bed"),
        ("twin", "Twin Bed"),
        ("soft", "Soft Bed"),
        ("standard", "Standard Bed"),
        ("king", "King Bed"),
        ("queen", "Queen Bed"),
        ("1k_2t", "1 King or 2 Twin Bed"),
        ("1q_2t", "1 Queen or 2 Twin Bed"),
    ]

    bed_type = models.CharField(max_length=20, choices=BED_CHOICES)

    VIEW_CHOICES = [
        ("no", "No View"),
        ("sea", "Sea"),
        ("valley", "Valley"),
        ("hill", "Hill"),
        ("pool", "Pool"),
        ("garden", "Garden"),
        ("lake", "Lake"),
        ("forest", "Forest"),
        ("palace", "Palace"),
        ("beach", "Beach"),
        ("mountain", "Mountain"),
        ("airport", "Airport"),
        ("harbor", "Harbor"),
    ]

    view_type = models.CharField(max_length=20, choices=VIEW_CHOICES)

    SMOKING_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    smoking_allowed = models.CharField(max_length=5, choices=SMOKING_CHOICES)

    # ---------------- EXTRA BED ----------------
    extra_bed_allowed = models.BooleanField(default=False)

    EXTRA_BED_TYPE = [
        ("mattress", "Mattress"),
        ("cot", "Cot"),
        ("sofa", "Sofa Cum Bed"),
    ]

    extra_bed_type = models.CharField(max_length=20, choices=EXTRA_BED_TYPE, blank=True, null=True)

    # ---------------- ROOM OCCUPANCY ----------------
    base_adult = models.PositiveIntegerField(default=2)
    min_adult = models.PositiveIntegerField(default=1)
    min_child = models.PositiveIntegerField(default=0)
    max_occupancy = models.PositiveIntegerField()

    # ---------------- PRICING ----------------
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    extra_adult_charge = models.DecimalField(max_digits=10, decimal_places=2)
    child_charge = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.property_name} - {self.room_name}"
    
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
class HotelImage(models.Model):
    hotel = models.ForeignKey("Hotel", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="hotel_images/")
    is_cover = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.hotel.property_name} Image"
    
    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            img = img.convert("RGB")
            img.thumbnail((1200, 800))  # Resize

            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=70)

            self.image.save(
                self.image.name,
                ContentFile(buffer.getvalue()),
                save=False
            )

        super().save(*args, **kwargs)