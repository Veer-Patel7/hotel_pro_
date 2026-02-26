from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path("dashboard/", views.hotel_dashboard, name="hotel_dashboard"),
    # path('register/', views.register_hotel, name="register_hotel"),
    path("basic-info/", views.basic_info, name="basic_info"),
    path("location/", views.location_page, name="location_page"),
    path("amenities/", views.amenities_page, name="amenities_page"),
    path("room/", views.room_page, name="room_page"),
    path("pictures/", views.picture_page, name="picture_page"),
    path("pictures/", views.picture_page, name="picture_page"),
    path("pictures/delete/<int:image_id>/", views.delete_image, name="delete_image"),
    path("pictures/cover/<int:image_id>/", views.set_cover, name="set_cover"),
    path("final-submission/", views.final_submission, name="final_submission"),

    #------------------MANAGE_ROOM---------------------------------------------- 
    path("manage-rooms/", views.manage_rooms, name="manage_rooms"),
    path("edit-room/<int:room_id>/", views.edit_room, name="edit_room"),
    path("delete-room/<int:room_id>/", views.delete_room, name="delete_room"),

    #---------------- REVIEW --------------------------------------------------
    
    path("reviews/", views.hotel_reviews),
    path("request-delete/<int:id>/", views.request_delete_review),
]
