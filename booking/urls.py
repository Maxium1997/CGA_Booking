from django.urls import path, re_path, include

from booking.views.booking.views import IndexView, MyBookingsView, BookingDetailView
from booking.views.booking.views import booking_paid, booking_check_out, booking_cancel
from booking.views.guest.views import GuestMemberEditionView
from booking.views.guest.views import guest_addition, guest_remove

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('my_bookings/', include([
        path('tabs', MyBookingsView.as_view(), name='my_bookings'),
        path('booking/', include([
            path('<pk>/', include([
                path('detail', BookingDetailView.as_view(), name='booking_detail'),
                path('paid', booking_paid, name='booking_paid'),
                path('check_out', booking_check_out, name='booking_check_out'),
                path('cancel', booking_cancel, name='booking_cancel'),
                path('guest/', include([
                    path('edit', GuestMemberEditionView.as_view(), name='guest_edit'),
                    path('add', guest_addition, name='guest_addition'),
                    path('remove/<guest_pk>', guest_remove, name='guest_remove'),
                ]))
            ])),
        ])),
    ])),
]
