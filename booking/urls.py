from django.urls import path, include

from booking.views import IndexView, MyBookingsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('my_bookings', MyBookingsView.as_view(), name='my_bookings'),
]
