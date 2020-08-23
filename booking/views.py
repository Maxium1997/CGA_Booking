from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from room.models import Hotel, Room
from booking.models import Booking, Guest
from booking.forms import BookingForm, GuestInfoForm
from booking.definition import Use
from booking.decorator import check_time_is_valid
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


@method_decorator(login_required, name='dispatch')
class BookingView(View):
    def get(self, request, slug, pk):
        hotel = get_object_or_404(Hotel, slug=slug)
        room = get_object_or_404(Room, pk=pk)

        guest_info_forms = [GuestInfoForm(prefix=str(x)) for x in range(5)]

        template = 'booking.html'
        context = {'hotel': hotel,
                   'room': room,
                   'uses': Use.__members__.values(),
                   'booking_form': BookingForm(),
                   'guest_info_forms': guest_info_forms}

        return render(request, template, context)

    def post(self, request, slug, pk):
        hotel = get_object_or_404(Hotel, slug=slug)
        room = get_object_or_404(Room, pk=pk)

        booking_form = BookingForm(request.POST)

        if check_time_is_valid(room, booking_form['check_in_time'].data, booking_form['days'].data):
            if booking_form.is_valid():
                new_booking = Booking.objects.create(unit_of_applicant=booking_form['unit_of_applicant'].data,
                                                     applicant=request.user,
                                                     use=booking_form['use'].data,
                                                     check_in_time=datetime.strptime((booking_form['check_in_time'].data+" 15:00"), '%Y-%m-%d %H:%M'),
                                                     check_out_time=datetime.strptime((booking_form['check_in_time'].data+" 12:00"), '%Y-%m-%d %H:%M') + timedelta(days=int(booking_form['days'].data)),
                                                     booked_room=room)
                new_booking.save()

                guest_info_forms = [GuestInfoForm(request.POST, prefix=str(x)) for x in range(5)]

                for guest_info_form in guest_info_forms:
                    data = [guest_info_form['name'].data,
                            guest_info_form['ID_Number'].data,
                            guest_info_form['rank'].data,
                            guest_info_form['relationship'].data,
                            guest_info_form['gender'].data,
                            guest_info_form['date_of_birth'].data,
                            guest_info_form['phone'].data,
                            guest_info_form['license_plate'].data]

                    if all(data):
                        new_guest = Guest.objects.create(booking_source=new_booking,
                                                         name=guest_info_form['name'].data,
                                                         ID_Number=guest_info_form['ID_Number'].data,
                                                         rank=guest_info_form['rank'].data,
                                                         relationship=guest_info_form['relationship'].data,
                                                         gender=guest_info_form['gender'].data,
                                                         date_of_birth=datetime.strptime(guest_info_form['date_of_birth'].data, '%Y/%m/%d'),
                                                         phone=guest_info_form['phone'].data,
                                                         licence_plate=guest_info_form['license_plate'].data)
                        new_guest.save()

            messages.success(request, "Booked Successfully.")
            return redirect('index')    # Modified to 'my_bookings' after
        else:
            guest_info_forms = [GuestInfoForm(request.POST, prefix=str(x)) for x in range(5)]

            template = 'booking.html'
            context = {'hotel': hotel,
                       'room': room,
                       'uses': Use.__members__.values(),
                       'booking_form': BookingForm(request.POST),
                       'guest_info_forms': guest_info_forms}

            messages.warning(request, "Time Conflict.")
            return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class MyBookingsView(View):
    def get(self, request):
        past = Booking.objects.filter(applicant=request.user, check_out_time__lt=datetime.now())
        future = Booking.objects.filter(applicant=request.user, check_in_time__gt=datetime.now())
        canceled = Booking.objects.filter(applicant=request.user, state=3)

        template = 'my_bookings.html'
        context = {'past_bookings': past,
                   'future_bookings': future,
                   'canceled_bookings': canceled}

        return render(request, template, context)
