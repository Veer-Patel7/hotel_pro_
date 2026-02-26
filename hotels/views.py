from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Hotel, Room, RoomCategory, RoomAvailability, HotelImage
from reviews.models import Review
from .forms import RoomForm, RoomCategoryForm, HotelBasicInfoForm, HotelLocationForm, HotelAmenitiesForm, HotelImageForm
from django.views.decorators.csrf import csrf_exempt



@login_required
def basic_info(request):

    hotel = Hotel.objects.filter(owner=request.user).first()

    if request.method == "POST":
        form = HotelBasicInfoForm(request.POST, instance=hotel)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            return redirect("hotels:location_page")  # next page
    else:
        form = HotelBasicInfoForm(instance=hotel)

    return render(request, "hotels/basic_info.html", {"form": form})

@login_required
def location_page(request):

    hotel = Hotel.objects.filter(owner=request.user).first()

    if not hotel:
        return redirect("hotels:basic_info")

    if request.method == "POST":
        form = HotelLocationForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect("hotels:amenities_page")  # next step
    else:
        form = HotelLocationForm(instance=hotel)

    return render(request, "hotels/location_page.html", {"form": form})

@login_required
def amenities_page(request):

    hotel = Hotel.objects.filter(owner=request.user).first()

    if not hotel:
        return redirect("hotels:basic_info")

    if request.method == "POST":
        form = HotelAmenitiesForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect("hotels:room_page")  # next step
    else:
        form = HotelAmenitiesForm(instance=hotel)

    return render(request, "hotels/amenities_page.html", {"form": form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hotel, Room, HotelImage  # adjust import if needed


@login_required(login_url="/hotel/login/")
def hotel_dashboard(request):

    # Latest hotel created by owner
    hotel = Hotel.objects.filter(owner=request.user).order_by("-id").first()

    if not hotel:
        return redirect("/hotel/register/")

    # Status Handling
    if hotel.status == "pending":
        return render(request, "hotels/waiting.html")

    if hotel.status == "rejected":
        return render(request, "hotels/rejected.html")

    if hotel.status == "blocked":
        return HttpResponse("Hotel Blocked")

    # If Approved → show dashboard
    if hotel.status == "approved":

        # Step Completion Checks
        rooms_count = Room.objects.filter(hotel=hotel).count()
        images_count = HotelImage.objects.filter(hotel=hotel).count()

        context = {
            "hotel": hotel,
            "rooms_completed": rooms_count > 0,
            "images_completed": images_count >= 3,
            "rooms_count": rooms_count,
            "images_count": images_count,
        }

        return render(request, "hotels/hotel_dashboard.html", context)

    return redirect("/hotel/register/")
# @login_required(login_url="/hotel/login/")
# def register_hotel(request):

#     user = request.user

#     # check if already has hotel
#     hotel = Hotel.objects.filter(owner=user).first()
#     if hotel:
#         return redirect('hotels:hotel_dashboard', hotel_id=hotel.id)

#     if request.method == "POST":
#         name = request.POST.get("hotel_name")
#         location = request.POST.get("location")
#         id1 = request.FILES.get("id1")
#         id2 = request.FILES.get("id2")

#         Hotel.objects.create(
#             owner=user,
#             hotel_name=name,
#             location=location,
#             id_proof1=id1,
#             id_proof2=id2,
#             status='pending'
#         )

#         return redirect('hotels:hotel_dashboard')

#     return render(request, "hotels/register_hotel.html")
@login_required
def room_page(request):

    hotel = Hotel.objects.filter(owner=request.user).first()

    if not hotel:
        return redirect("hotels:basic_info")

    if request.method == "POST":
        form = RoomCategoryForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect("hotels:picture_page")  # stay on page to add more rooms
    else:
        form = RoomCategoryForm()

    rooms = RoomCategory.objects.filter(hotel=hotel)

    return render(request, "hotels/room_page.html", {
        "form": form,
        "rooms": rooms
    })
    
@login_required
def picture_page(request):
    hotel = Hotel.objects.filter(owner=request.user).first()

    if not hotel:
        return redirect("hotels:basic_info")

    images = HotelImage.objects.filter(hotel=hotel)

    image_count = images.count()
    can_submit = image_count >= 3

    if request.method == "POST":
        files = request.FILES.getlist("images")

        for file in files:
            HotelImage.objects.create(
                hotel=hotel,
                image=file,
                order=image_count
            )
            image_count += 1

        return redirect("hotels:picture_page")

    return render(request, "hotels/picture_page.html", {
        "images": images,
        "can_submit": can_submit,
        "image_count": image_count
    })


@login_required
def delete_image(request, image_id):
    image = HotelImage.objects.get(id=image_id)
    image.delete()
    return redirect("hotels:picture_page")


@login_required
def set_cover(request, image_id):
    hotel = Hotel.objects.filter(owner=request.user).first()

    HotelImage.objects.filter(hotel=hotel).update(is_cover=False)

    image = HotelImage.objects.get(id=image_id)
    image.is_cover = True
    image.order = 0
    image.save()

    return redirect("hotels:picture_page")

# ==============================
# MANAGE ROOMS (List + Add)
# ==============================
@login_required
def manage_rooms(request):

    if request.user.role != "hotel_admin":
        messages.error(request, "Access Denied")
        return redirect("home")

    hotel = Hotel.objects.filter(owner=request.user, status="approved").first()

    if not hotel:
        messages.warning(request, "Please register your hotel first.")
        return redirect("hotels:hotel_dashboard")

    categories = RoomCategory.objects.filter(hotel=hotel)
    rooms = Room.objects.filter(hotel=hotel)

    category_form = RoomCategoryForm()
    room_form = RoomForm(hotel=hotel)

    if request.method == "POST":

        if "add_category" in request.POST:
            category_form = RoomCategoryForm(request.POST)
            if category_form.is_valid():
                category = category_form.save(commit=False)
                category.hotel = hotel
                category.save()
                messages.success(request, "Room category added!")
                return redirect("hotels:manage_rooms")

        elif "add_room" in request.POST:
            room_form = RoomForm(request.POST, hotel=hotel)
            if room_form.is_valid():
                room = room_form.save(commit=False)
                room.hotel = hotel
                room.save()
                messages.success(request, "Room added!")
                return redirect("hotels:manage_rooms")

    return render(request, "hotels/manage_rooms.html", {
        "hotel": hotel,
        "categories": categories,
        "rooms": rooms,
        "category_form": category_form,
        "room_form": room_form,
    })


# ==============================
# EDIT ROOM
# ==============================
@login_required
def edit_room(request, room_id):

    if request.user.role != "hotel_admin":
        messages.error(request, "Access Denied")
        return redirect("home")

    hotel = Hotel.objects.filter(owner=request.user, status="approved").first()

    if not hotel:
        messages.warning(request, "Hotel not found.")
        return redirect("hotels:hotel_dashboard")

    room = get_object_or_404(Room, id=room_id, hotel=hotel)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room, hotel=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully!")
            return redirect("hotels:manage_rooms")
    else:
        form = RoomForm(instance=room, hotel=hotel)

    return render(request, "hotels/edit_room.html", {
        "form": form,
        "hotel": hotel
    })


# ==============================
# DELETE ROOM
# ==============================
@login_required
def delete_room(request, room_id):

    if request.user.role != "hotel_admin":
        messages.error(request, "Access Denied")
        return redirect("home")

    hotel = Hotel.objects.filter(owner=request.user, status="approved").first()

    if not hotel:
        messages.warning(request, "Hotel not found.")
        return redirect("hotels:hotel_dashboard")

    room = get_object_or_404(Room, id=room_id, hotel=hotel)

    room.delete()
    messages.success(request, "Room deleted successfully!")

    return redirect("hotels:manage_rooms")

#----------review-------------

@login_required(login_url="/hotel/login/")
def hotel_reviews(request):

    reviews = Review.objects.filter(hotel__owner=request.user)

    return render(request, "hotels/reviews.html", {"reviews": reviews})


@login_required(login_url="/hotel/login/")
def request_delete_review(request, id):

    r = Review.objects.get(id=id)

    if r.hotel.owner != request.user:
        return HttpResponse("Unauthorized")

    r.status = "delete_request"
    r.save()

    return redirect("/hotel/reviews/")

@login_required
def final_submission(request):

    hotel = Hotel.objects.filter(owner=request.user).first()

    if not hotel:
        return redirect("hotels:basic_info")

    images = HotelImage.objects.filter(hotel=hotel)
    rooms = RoomCategory.objects.filter(hotel=hotel)

    if images.count() < 3 & images.count() > 5:
        return redirect("hotels:picture_page")

    if request.method == "POST":
        hotel.status = "submitted"
        hotel.save()
        return render(request, "hotels/hotel_dashboard.html")  # or success page

    return render(request, "hotels/final_submission.html", {
        "hotel": hotel,
        "images": images,
        "rooms": rooms
    })