from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView, View, TemplateView

from booking.models import Booking, Guest
from booking.definition import State
from booking.forms import GuestInfoForm, BookingForm
from booking.decorator import guest_form_to_Guest, calculate_booking_price


@method_decorator(login_required, name='dispatch')
class GuestMemberEditionView(TemplateView):
    template_name = 'guest/edit.html'

    def dispatch(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs['pk'])
        if booking.applicant != request.user:
            messages.warning(request, "Request Rejected. You are not this booking applicant.")
        elif booking.state != State.Outstanding.value[0]:
            messages.warning(request, "Request Rejected. This booking is not outstanding.")
            return redirect('my_bookings')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['booking'] = booking
        context['guest_info_form'] = GuestInfoForm()
        return context


def guest_addition(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.applicant != request.user:
        messages.warning(request, "Request Rejected. You are not this booking applicant.")
    elif booking.state != State.Outstanding.value[0]:
        messages.warning(request, "Request Rejected. This booking is not outstanding.")
        return redirect('my_bookings')

    guest_info_form = GuestInfoForm(request.POST)
    if guest_form_to_Guest(guest_info_form, booking):
        calculate_booking_price(booking)
        messages.success(request, "Guest Added Successfully.")
        return redirect('guest_edit', pk=pk)
    else:
        messages.warning(request, "Please check out your offer form.")
        template = 'guest/edit.html'
        context = {'booking': booking,
                   'guest_info_form': GuestInfoForm(request.POST)}
        return render(request, template, context)
