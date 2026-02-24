from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from reviews.models import Review
from hotels.models import Hotel


# @login_required(login_url="/login/")
# def dashboard(request):
#     return render(request, "customer/dashboard.html")

# ================= NORMAL VIEWS =================
def customer_search(request):
    hotels = Hotel.objects.all()

    location = request.GET.get("location")

    if location:
        hotels = Hotel.objects.filter(city__icontains=location)

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