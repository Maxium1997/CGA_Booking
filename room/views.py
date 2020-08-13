from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from registration.definition import Identity
from room.models import Hotel
from room.forms import HotelForm
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
    form_class = HotelForm
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


# @method_decorator(login_required, name='dispatch')
# class HotelEditionView(View):
#

@method_decorator(login_required, name='dispatch')
class OwnedHotelView(ListView):
    model = Hotel
    template_name = 'hotel/owned.html'
    context_object_name = 'my_hotels'

    def dispatch(self, request, *args, **kwargs):
        if request.user.identity != Identity.Proprietor.value[0]:
            messages.warning(request, "Request Reject, you are not proprietor")
            return redirect('hotels')
        return super(OwnedHotelView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Hotel.objects.filter(owner=self.request.user)


class HotelDetailView(View):
    def get(self, request, slug):
        hotel = get_object_or_404(Hotel, slug=slug)
        template = 'hotel/detail.html'
        context = {
            'hotel': hotel,
            'hotels': Hotel.objects.all(),
            'rooms': hotel.room_set.all()
        }
        return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class HotelEditionView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.identity != Identity.Proprietor.value[0]:
            raise PermissionDenied
        return super(HotelEditionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, slug):
        hotel = get_object_or_404(Hotel, slug=slug)

        if hotel.owner != request.user:
            messages.error(request, "Permission Denied. You are not this hotel owner.")
            return redirect('hotels')

        template = 'hotel/edition.html'
        context = {'form': HotelForm(instance=hotel)}

        return render(request, template, context)

    def post(self, request, slug):
        hotel = get_object_or_404(Hotel, slug=slug)

        if hotel.owner != request.user:
            messages.error(request, "Permission Denied. You are not this hotel owner.")
            return redirect('hotels')

        hotel = HotelForm(request.POST, request.FILES, instance=hotel).save(commit=False)
        hotel.photo_upload(hotel.external_appearance)
        messages.success(request, "Successfully Edit.")
        return redirect('my_hotels')
