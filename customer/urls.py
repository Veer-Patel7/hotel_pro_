from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
urlpatterns = [
    # Customer homepage
    path('', views.customer_search, name='customer_search'),

    # Hotel and Room details
    # path('hotel/<int:hotel_id>/', views.hotel_detail, name="hotel_detail"),
    path('room/<int:room_id>/', views.room_select, name="room_select"),
    path('search_hotel/', views.search_results, name='search_results'),
    # Booking details
    path('hotel/', views.hotel_list, name='hotel_list'),

    # Review add
    path('add-review/<int:hotel_id>/', views.add_review, name="add_review"),
]
