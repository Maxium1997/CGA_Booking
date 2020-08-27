from django.urls import path, include

from booking.views import IndexView, MyBookingsView, BookingDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('my_bookings/', include([
        path('tabs', MyBookingsView.as_view(), name='my_bookings'),
        path('<pk>', BookingDetailView.as_view(), name='booking_detail'),
    ])),
]
