from datetime import datetime, timedelta
from room.models import Room
from booking.models import Booking


def check_time_is_valid(room, check_in_time, days):
    tmp_str = ""
    # cit = check in time
    # cot = check out time
    cit = datetime.strptime((check_in_time + " 15:00"), '%Y-%m-%d %H:%M')
    cot = cit + timedelta(days=int(days), hours=-3)

    for booking in room.booking_set.all():
        # bcit = booking check in time
        # bcot = booking check out time
        bcit = booking.check_in_time
        bcot = booking.check_out_time
        if bcit <= cit <= bcot or bcit <= cot <= bcot or cit <= bcit <= bcot <= cot:
            return False

    return True


def calculate_booking_price(booking: Booking):
    guest_num = booking.guest_set.all().count()
    pass
