from django.urls import path, include

from room.views import HotelsView, HotelCreationView, OwnedHotelView, HotelDetailView, HotelEditionView

urlpatterns = [
    path('hotel/', include([
        path('list', HotelsView.as_view(), name='hotels'),
        path('creation', HotelCreationView.as_view(), name='hotel_creation'),
        path('owned', OwnedHotelView.as_view(), name='my_hotels'),
        path('<slug:slug>/', include([
            path('edition', HotelEditionView.as_view(), name='hotel_edition'),
            path('detail', HotelDetailView.as_view(), name='hotel_detail'),
        ])),
    ]))
]
