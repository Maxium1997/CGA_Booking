from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
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


@method_decorator(login_required, name='dispatch')
class OwnedHotelView(ListView):
    model = Hotel
    template_name = 'hotel/owned.html'
    context_object_name = 'my_hotels'

    def dispatch(self, request, *args, **kwargs):
        if request.user.identity != Identity.Proprietor.value[0]:
            raise PermissionDenied
        return super(OwnedHotelView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Hotel.objects.filter(owner=self.request.user)


class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotel/detail.html'

    def get_context_data(self, **kwargs):
        obj = super(HotelDetailView, self).get_object()
        kwargs['hotels'] = Hotel.objects.exclude(name=obj.name)[:4]
        return super(HotelDetailView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class HotelEditionView(UpdateView):
    model = Hotel
    template_name = 'hotel/edition.html'
    fields = ['external_appearance', 'name', 'slug', 'address', 'phone', 'website', 'introduction']

    def dispatch(self, request, *args, **kwargs):
        obj = super(HotelEditionView, self).get_object()
        if obj.owner != request.user:
            raise PermissionDenied
        return super(HotelEditionView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        obj = super(HotelEditionView, self).get_object()
        kwargs['form'] = HotelForm(instance=obj)
        return super(HotelEditionView, self).get_context_data(**kwargs)
