from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path("dashboard/", views.hotel_dashboard, name="hotel_dashboard"),
    path('register/', views.register_hotel, name="register_hotel"),

    #------------------MANAGE_ROOM---------------------------------------------- 
    path("manage-rooms/", views.manage_rooms, name="manage_rooms"),
    path("edit-room/<int:room_id>/", views.edit_room, name="edit_room"),
    path("delete-room/<int:room_id>/", views.delete_room, name="delete_room"),

    #---------------- REVIEW --------------------------------------------------
    
    path("reviews/", views.hotel_reviews),
    path("request-delete/<int:id>/", views.request_delete_review),
]
