from django.urls import path, include

from booking.views.booking.views import IndexView, MyBookingsView, BookingDetailView
from booking.views.booking.views import BookingCheckOut, BookingCancel
from booking.views.guest.views import EditGuestMemberView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('my_bookings/', include([
        path('tabs', MyBookingsView.as_view(), name='my_bookings'),
        # path('<pk>', BookingDetailView.as_view(), name='booking_detail'),
        path('<pk>/', include([
            path('detail', BookingDetailView.as_view(), name='booking_detail'),
            path('check_out', BookingCheckOut.as_view(), name='booking_check_out'),
            path('cancel', BookingCancel.as_view(), name='booking_cancel'),
            path('guest_edit', EditGuestMemberView.as_view(), name='guest_edit'),
        ])),
    ])),
]
