from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from registration.definition import Identity
from room.models import Hotel, Room, Dormitory
from room.forms import RoomForm, DormitorySettingForm


@method_decorator(login_required, name='dispatch')
class RoomCreationView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.identity != Identity.Proprietor.value[0]:
            raise PermissionDenied
        return super(RoomCreationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, slug):
        hotel = get_object_or_404(Hotel, slug=slug)

        if hotel.owner != request.user:
            messages.error(request, "Permission Denied. You are not this hotel owner.")
            return redirect('hotels')

        template = 'room/creation.html'
        context = {'hotel': hotel,
                   'room_form': RoomForm(),
                   'dormitory_setting_form': DormitorySettingForm()}

        return render(request, template, context)

    def post(self, request, slug):
        hotel = get_object_or_404(Hotel, slug=slug)
        room_form = RoomForm(request.POST, instance=Room())
        dormitory_setting_form = DormitorySettingForm(request.POST, instance=Dormitory())

        if room_form.is_valid():
            new_room = room_form.save(commit=False)
            new_room.hotel = hotel
            new_room.save()
            if dormitory_setting_form.is_valid():
                new_dormitory_setting = dormitory_setting_form.save(commit=False)
                new_dormitory_setting.room = new_room
                new_dormitory_setting.save()
            messages.success(request, "Successfully added new room")
            return redirect('hotel_detail', slug=hotel.slug)

        template = 'room/creation.html'
        context = {'hotel': hotel,
                   'room_form': RoomForm(),
                   'dormitory_setting_form': DormitorySettingForm()}

        return render(request, template, context)
