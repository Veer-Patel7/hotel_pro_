from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from reviews.models import Review
from hotels.models import Hotel, Room
from django.db.models import Min, Max


# @login_required(login_url="/login/")
# def dashboard(request):
#     return render(request, "customer/dashboard.html")

# ================= NORMAL VIEWS =================
def customer_search(request):

    hotels = Hotel.objects.all()

    if request.method == "POST":
        location = request.POST.get("location")

        if location:
            hotels = hotels.filter(city__icontains=location)

    # Annotate min and max price from RoomCategory
    hotels = hotels.annotate(
        min_price=Min("room_categories__base_rate"),
        max_price=Max("room_categories__base_rate")
    )

    return render(request, "customer/search.html", {
        "hotels": hotels
    })
# def customer_search(request):
#     hotels = Hotel.objects.filter(is_approved=True, is_blocked=False)
#     return render(request, 'customer/search.html', {'hotels': hotels})

def search_results(request):

    if request.method == "POST":
        location = request.POST.get('location')

        hotels = Hotel.objects.filter(
            status=True,  # if approved  # is_approved=True, is_blocked=False,
            location__icontains=location
        )
    else:
        hotels = Hotel.objects.filter(
            status=True,  # if approved  #is_approved=True,is_blocked=False
        )
    
    return render(request, 'customer/search_results.html', {
        'hotels': hotels
    })


def hotel_list(request):
    hotels = Hotel.objects.filter(is_approved=True, is_blocked=False)
    return render(request, "customer/hotel_list.html", {'hotels': hotels})

def room_select(request, room_id):
    return render(request, "customer/room_select.html", {"room_id": room_id})

def hotel_detail(request, pk):

    hotel = get_object_or_404(Hotel, pk=pk)

    # Show only available rooms
    available_rooms = Room.objects.filter(
        hotel=hotel,
        status="available"
    ).select_related("category")

    # Minimum price
    min_price = available_rooms.aggregate(
        Min("category__price_per_night")
    )["category__price_per_night__min"]

    context = {
        "hotel": hotel,
        "rooms": available_rooms,
        "min_price": min_price,
    }

    return render(request, "customer/hotel_detail.html", context)

@login_required(login_url="/login/")
def booking_details(request):
    
    return render(request, "customer/booking_details.html")

@login_required(login_url="/login/")
def add_review(request, hotel_id):

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        recommend = request.POST.get("recommend")

        Review.objects.create(
            hotel_id=hotel_id,
            user=request.user,
            rating=rating,
            comment=comment,
            recommend=True if recommend == "yes" else False
        )

        return redirect("/")

    return render(request, "customer/add_review.html")