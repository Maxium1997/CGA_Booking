from django.urls import path, include

from booking.views import IndexView, MyBookingsView, BookingDetailView
from booking.views import BookingCheckOut, BookingCancel

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('my_bookings/', include([
        path('tabs', MyBookingsView.as_view(), name='my_bookings'),
        # path('<pk>', BookingDetailView.as_view(), name='booking_detail'),
        path('<pk>/', include([
            path('detail', BookingDetailView.as_view(), name='booking_detail'),
            path('check_out', BookingCheckOut.as_view(), name='booking_check_out'),
            path('cancel', BookingCancel.as_view(), name='booking_cancel'),
        ])),
    ])),
]
