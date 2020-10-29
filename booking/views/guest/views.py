from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView

from booking.models import Booking, Guest
from booking.definition import State
from booking.forms import GuestInfoForm
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
        return context


def __booking_check(request, booking: Booking):
    if booking.applicant != request.user:
        messages.warning(request, "Request Rejected. You are not this booking applicant.")
    elif booking.state != State.Outstanding.value[0]:
        messages.warning(request, "Request Rejected. This booking is not outstanding.")
    return redirect('my_bookings')


class GuestAdditionView(View):
    model = Guest
    form_class = GuestInfoForm
    template_name = 'guest/add.html'

    def get(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs['pk'])
        template = 'guest/add.html'
        context = {'booking': booking,
                   'form': GuestInfoForm(booking_source=booking)}

        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs['pk'])

        if booking.applicant != request.user:
            messages.warning(request, "Request Rejected. You are not this booking applicant.")
            return redirect('my_bookings')
        elif booking.state != State.Outstanding.value[0]:
            messages.warning(request, "Request Rejected. This booking is not outstanding.")
            return redirect('my_bookings')
        else:
            pass

        guest_info_form = GuestInfoForm(request.POST, booking_source=booking)

        if guest_form_to_Guest(guest_info_form, booking):
            booking.total_price = calculate_booking_price(booking)
            booking.save()
            messages.success(request, "Guest Added Successfully.")
            return redirect('guest_edit', pk=kwargs['pk'])
        else:
            messages.warning(request, "Please check out your offer form.")
            template = 'guest/add.html'
            context = {'booking': booking,
                       'form': GuestInfoForm(request.POST, booking_source=booking)}
            return render(request, template, context)


def guest_remove(request, pk, guest_pk):
    booking = get_object_or_404(Booking, pk=pk)

    __booking_check(request, booking)

    if booking.applicant != request.user:
        messages.warning(request, "You have no permission to remove the guest.")
        return redirect('my_bookings')
    else:
        if booking.guest_set.all().count() == 1:
            messages.warning(request, "The guest is last one, you cannot remove it.")
        else:
            Guest.objects.get(pk=guest_pk).delete()
            booking.total_price = calculate_booking_price(booking)
            booking.save()
            messages.success(request, "Guest Removed Successfully.")
        return redirect(request.META.get('HTTP_REFERER'))
