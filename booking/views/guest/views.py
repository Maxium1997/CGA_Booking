from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView, View

from booking.models import Booking, Guest
from booking.definition import State
from booking.forms import GuestInfoForm, BookingForm


@method_decorator(login_required, name='dispatch')
class EditGuestMemberView(View):
    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)

        if booking.state != State.Outstanding.value[0]:
            messages.warning(request, "Request Rejected.")
            return redirect('my_bookings')

        else:
            template = 'guest/edit.html'
            context = {'booking': booking}
            return render(request, template, context)
