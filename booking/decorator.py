from datetime import datetime, timedelta
from room.models import Room
from booking.models import Booking
from booking.definition import Use


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


def calculate_booking_price(booking: Booking, days: int):
    washing_fee = booking.booked_room.dormitory.washing_fee
    usage_fee = booking.booked_room.dormitory.usage_fee
    utility_bill = booking.booked_room.dormitory.utility_bill

    single_bed_num = booking.booked_room.single_bed
    double_bed_num = booking.booked_room.double_bed
    max_guest_num = single_bed_num + double_bed_num*2

    guest_num = booking.guest_set.all().count()

    total_price = 0

    if booking.use == Use.OfficialBusiness.value[0] or booking.use == Use.Guidance.value[0]:
        if guest_num >= (single_bed_num + double_bed_num * 2):
            total_price += washing_fee * single_bed_num + washing_fee * double_bed_num
        else:
            total_price += washing_fee * guest_num
    else:
        total_price += (usage_fee + utility_bill) * days
        if guest_num >= (single_bed_num + double_bed_num * 2):
            total_price += washing_fee * single_bed_num + washing_fee * double_bed_num
        else:
            total_price += washing_fee * guest_num

    return total_price


def automatic_collate():
    pass
