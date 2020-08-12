from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from registration.definition import Identity
from room.models import Hotel
from room.forms import HotelCreationForm
# Create your views here.


class HotelsView(ListView):
    model = Hotel
    queryset = Hotel.objects.all()
    template_name = 'hotel/hotels.html'
    context_object_name = 'hotels'


@method_decorator(login_required, name='dispatch')
class HotelCreationView(CreateView):
    model = Hotel
    template_name = 'hotel/creation.html'
    form_class = HotelCreationForm
    context_object_name = 'hotel'

    def dispatch(self, request, *args, **kwargs):
        if request.user.identity != Identity.Proprietor.value[0]:
            raise PermissionDenied
        return super(HotelCreationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        hotel = form.save(commit=False)
        hotel.owner = self.request.user
        hotel.photo_upload(form.cleaned_data['external_appearance'])
        hotel.save()
        return redirect('hotels')
