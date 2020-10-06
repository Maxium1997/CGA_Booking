from django.urls import path, include

from room.views.hotel.views import HotelsView, HotelCreationView, OwnedHotelView, HotelDetailView, HotelEditionView, HotelTransferView
from room.views.room.views import RoomCreationView, RoomEditionView, OwnedRoomView, RoomDetailView
from room.views.room.views import room_photo_upload

from booking.views.booking.views import BookingView

urlpatterns = [
    path('hotel/', include([
        path('list', HotelsView.as_view(), name='hotels'),
        path('creation', HotelCreationView.as_view(), name='hotel_creation'),
        path('owned', OwnedHotelView.as_view(), name='my_hotels'),

        path('<slug:slug>/', include([
            path('transfer', HotelTransferView.as_view(), name='hotel_transfer'),
            path('edition', HotelEditionView.as_view(), name='hotel_edition'),
            path('detail', HotelDetailView.as_view(), name='hotel_detail'),

            path('room/', include([
                path('creation', RoomCreationView.as_view(), name='room_creation'),
                path('owned', OwnedRoomView.as_view(), name='my_rooms'),

                path('<pk>/', include([
                    path('edition', RoomEditionView.as_view(), name='room_edition'),
                    path('detail', RoomDetailView.as_view(), name='room_detail'),
                    path('booking', BookingView.as_view(), name='booking'),
                    path('photo/', include([
                        path('upload', room_photo_upload, name='room_photo_upload'),
                    ])),
                ])),
            ])),
        ])),
    ])),
]
