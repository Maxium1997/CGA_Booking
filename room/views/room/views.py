from os import listdir

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from CGA_Booking.settings import MEDIA_ROOT
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


@method_decorator(login_required, name='dispatch')
class RoomEditionView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.identity != Identity.Proprietor.value[0]:
            raise PermissionDenied
        return super(RoomEditionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, slug, pk):
        hotel = get_object_or_404(Hotel, slug=slug)
        room = get_object_or_404(Room, pk=pk)

        if hotel.owner != request.user:
            messages.error(request, "Permission Denied. You are not this hotel owner.")
            return redirect('hotels')

        template = 'room/edition.html'
        context = {'room': room,
                   'hotel': hotel,
                   'room_form': RoomForm(instance=room),
                   'dormitory_setting_form': DormitorySettingForm(instance=room.dormitory)}

        return render(request, template, context)

    def post(self, request, slug, pk):
        hotel = get_object_or_404(Hotel, slug=slug)
        room = get_object_or_404(Room, pk=pk)

        if hotel.owner != request.user:
            messages.error(request, "Permission Denied. You are not this hotel owner.")
            return redirect('hotels')

        room = RoomForm(request.POST, instance=room).save(commit=True)
        DormitorySettingForm(request.POST, instance=room.dormitory).save(commit=True)
        messages.success(request, "Successfully Edit.")
        return redirect('my_rooms', slug=hotel.slug)


@method_decorator(login_required, name='dispatch')
class OwnedRoomView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.identity != Identity.Proprietor.value[0]:
            messages.warning(request, "Request Reject, you are not proprietor")
            return redirect('hotels')
        return super(OwnedRoomView, self).dispatch(request, *args, **kwargs)

    def get(self, request, slug):
        hotel = get_object_or_404(Hotel, slug=slug)

        if hotel.owner != request.user:
            messages.error(request, "Permission Denied. You are not this hotel owner.")
            return redirect('hotels')

        template = 'room/owned.html'
        context = {'hotel': hotel,
                   'rooms': hotel.room_set.all()}

        return render(request, template, context)


class RoomDetailView(View):
    def get(self, request, slug, pk):
        hotel = get_object_or_404(Hotel, slug=slug)
        room = get_object_or_404(Room, pk=pk)

        photo_path_list = []

        album_path = MEDIA_ROOT + 'hotels/' + hotel.name + '/' + room.name

        try:
            for file in listdir(album_path):
                if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                    photo_path_list.append(
                        '/' + MEDIA_ROOT.split('/')[
                            -2] + '/hotels/' + hotel.name + '/' + room.name + '/' + file)
        except FileNotFoundError:
            pass

        template = 'room/detail.html'
        context = {'hotel': hotel,
                   'room': room,
                   'rooms': hotel.room_set.all(),
                   'photo_list': photo_path_list}

        return render(request, template, context)


@login_required
def room_photo_upload(request, slug, pk):
    hotel = get_object_or_404(Hotel, slug=slug)
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        if hotel.owner == request.user:
            try:
                photo = request.FILES.get('photo_file')
                room.photo_upload(photo)
                messages.success(request, "Successfully uploaded.")
            except AttributeError:
                pass

    return redirect('room_detail', slug=slug, pk=pk)

