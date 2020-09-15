from django import template

from registration.models import User
from room.models import Hotel

register = template.Library()


@register.filter(name='shorten_to')
def shorten_to(original_text: str, word_count: int):
    return original_text[0:word_count] + '...' if original_text else 'No introduction recently.'


@register.filter(name='is_hotel_owner')
def is_hotel_owner(user: User, hotel: Hotel):
    return True if hotel.owner == user else False


@register.filter(name='region')
def region(address: str):
    return address[:3]


@register.filter(name='lowest_price')
def lowest_price(hotel: Hotel):
    rooms = hotel.room_set.all()
    lowest_room = rooms[0]
    for room in rooms:
        if room.dormitory.get_price() < lowest_room.dormitory.get_price():
            lowest_room = room

    return lowest_room.dormitory.get_price()
