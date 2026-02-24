from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Hotel, Room, RoomCategory, RoomAvailability
from reviews.models import Review
from .forms import RoomForm, RoomCategoryForm




@login_required(login_url="/hotel/login/")
def hotel_dashboard(request):

    # Check if any approved hotel exists for this owner
    approved_hotel = Hotel.objects.filter(
        owner=request.user,
        status="approved"
    ).first()

    if approved_hotel:
        return render(
            request,
            "hotels/hotel_dashboard.html",
            {"hotel": approved_hotel}
        )

    # Get latest hotel request
    hotel = Hotel.objects.filter(
        owner=request.user
    ).order_by("-id").first()

    if not hotel:
        return redirect("/hotel/register/")

    if hotel.status == "pending":
        return render(request, "hotels/waiting.html")

    if hotel.status == "rejected":
        return render(request, "hotels/rejected.html")

    if hotel.status == "blocked":
        return HttpResponse("Hotel Blocked")

    return redirect("/hotel/register/")

@login_required(login_url="/hotel/login/")
def register_hotel(request):

    user = request.user

    # check if already has hotel
    hotel = Hotel.objects.filter(owner=user).first()
    if hotel:
        return redirect('hotels:hotel_dashboard', hotel_id=hotel.id)

    if request.method == "POST":
        name = request.POST.get("hotel_name")
        location = request.POST.get("location")
        id1 = request.FILES.get("id1")
        id2 = request.FILES.get("id2")

        Hotel.objects.create(
            owner=user,
            hotel_name=name,
            location=location,
            id_proof1=id1,
            id_proof2=id2,
            status='pending'
        )

        return redirect('hotels:hotel_dashboard')

    return render(request, "hotels/register_hotel.html")


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