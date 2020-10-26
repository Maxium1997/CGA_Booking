from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q

from registration.models import User
from registration.definition import Identity
from room.models import Hotel, Room
from booking.models import Booking, Guest
from booking.forms import BookingForm, GuestInfoForm
from booking.definition import Use, State
from booking.decorator import check_time_is_valid, calculate_booking_price, guest_form_to_Guest
from proclamation.models import Proclamation
from booking.mail import booking_notification_mail
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs['proclamations'] = Proclamation.objects.all()[:8]
        return super(IndexView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class BookingView(View):
    def get(self, request, slug, pk):
        try:
            hotel = get_object_or_404(Hotel, slug=slug)
            room = get_object_or_404(Room, pk=pk)

            template = 'booking.html'
            context = {'hotel': hotel,
                       'room': room,
                       'uses': Use.__members__.values(),
                       'booking_form': BookingForm(applicant=self.request.user)}

            return render(request, template, context)
        except:
            messages.warning(request, "Please update your officer information first.")
            return redirect('officer_index')

    def post(self, request, slug, pk):
        hotel = get_object_or_404(Hotel, slug=slug)
        room = get_object_or_404(Room, pk=pk)

        booking_form = BookingForm(request.POST, applicant=self.request.user)

        if check_time_is_valid(room, booking_form['check_in_time'].data, booking_form['days'].data):
            if booking_form.is_valid():
                new_booking = Booking.objects.create(unit_of_applicant=booking_form['unit_of_applicant'].data,
                                                     applicant=request.user,
                                                     use=booking_form['use'].data,
                                                     check_in_time=datetime.strptime((booking_form['check_in_time'].data+" 15:00"), '%Y-%m-%d %H:%M'),
                                                     check_out_time=datetime.strptime((booking_form['check_in_time'].data+" 12:00"), '%Y-%m-%d %H:%M') + timedelta(days=int(booking_form['days'].data)),
                                                     booked_room=room)
                new_booking.save()

                messages.success(request, "Booked Successfully.")
                # booking_notification_mail(hotel.owner, new_booking)
            return redirect('guest_edit', pk=new_booking.pk)
        else:
            messages.warning(request, "Time Conflict.")

            template = 'booking.html'
            context = {'hotel': hotel,
                       'room': room,
                       'uses': Use.__members__.values(),
                       'booking_form': BookingForm(request.POST, applicant=self.request.user)}

            return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class MyBookingsView(View):
    def get(self, request):
        template = 'booking/my_bookings.html'

        if request.user.identity == Identity.Traveler.value[0]:
            all_bookings = Booking.objects.filter(applicant=request.user)
        else:
            all_bookings = Booking.objects.filter(booked_room__hotel__owner=request.user)

        future_bookings = all_bookings.filter(check_in_time__gt=datetime.now()).exclude(state=State.Canceled.value[0])
        past_bookings = all_bookings.filter(check_out_time__lt=datetime.now(), state=State.CheckedOut.value[0])
        canceled_bookings = all_bookings.filter(state=State.Canceled.value[0])
        other_bookings = all_bookings.filter(check_out_time__lt=datetime.now()).exclude(Q(state=State.Canceled.value[0])|
                                                                                        Q(state=State.CheckedOut.value[0]))

        context = {'future_bookings': future_bookings,
                   'past_bookings': past_bookings,
                   'canceled_bookings': canceled_bookings,
                   'other_bookings': other_bookings,
                   'State': State.__members__}

        return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookingDetailView, self).get_context_data(**kwargs)
        context['uses'] = Use.__members__.values()
        context['guests'] = self.object.guest_set.all()
        return context


def booking_paid(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.user != booking.booked_room.hotel.owner:
        messages.warning(request, "You have no permission to modify the booking.")
    else:
        booking.state = State.Paid.value[0]
        booking.save()
        messages.success(request, "Modified Successfully.")
    return redirect(request.META.get('HTTP_REFERER'))


def booking_check_out(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.user == booking.booked_room.hotel.owner:
        if booking.state == State.Paid.value[0]:
            booking.state = State.CheckedOut.value[0]
            booking.save()
            messages.success(request, "Modified Successfully.")
        else:
            messages.warning(request, "This booking didn't paid, cannot turn the state to check out.")
    else:
        messages.warning(request, "You have no permission to modify the booking.")
    return redirect(request.META.get('HTTP_REFERER'))


def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.user == booking.applicant or request.user == booking.booked_room.hotel.owner:
        booking.state = State.Canceled.value[0]
        booking.save()
        messages.success(request, "Canceled Successfully.")
    else:
        messages.warning(request, "You have no permission to cancel the booking.")
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def booking_collection(request):
    user = User.objects.get(username=request.user.username)
    if user.identity == Identity.Traveler.value[0]:
        all_bookings = Booking.objects.filter(applicant=request.user)
    else:
        all_bookings = Booking.objects.filter(booked_room__hotel__owner=request.user)

    for booking in all_bookings:
        if booking.check_out_time < datetime.now() and booking.state != State.CheckedOut.value[0]:
            booking.state = State.Canceled.value[0]
            booking.save()

    return redirect('my_bookings')
