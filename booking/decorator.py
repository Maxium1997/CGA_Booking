from datetime import datetime, timedelta
from room.models import Room
from booking.models import Booking, Guest
from booking.definition import Use
from booking.forms import GuestInfoForm


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
    washing_fee = booking.booked_room.dormitory.washing_fee
    usage_fee = booking.booked_room.dormitory.usage_fee
    utility_bill = booking.booked_room.dormitory.utility_bill
    days = (booking.check_out_time.date() - booking.check_in_time.date()).days

    single_bed_num = booking.booked_room.single_bed
    double_bed_num = booking.booked_room.double_bed

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


def guest_form_to_Guest(guest_info_form: GuestInfoForm, booking: Booking):
    data = [guest_info_form['name'].data,
            guest_info_form['ID_Number'].data,
            guest_info_form['rank'].data,
            guest_info_form['relationship'].data,
            guest_info_form['gender'].data,
            guest_info_form['date_of_birth'].data,
            guest_info_form['phone'].data,
            guest_info_form['license_plate'].data]

    if all(data):
        try:
            new_guest = Guest.objects.create(booking_source=booking,
                                             name=guest_info_form['name'].data,
                                             ID_Number=guest_info_form['ID_Number'].data,
                                             rank=guest_info_form['rank'].data,
                                             relationship=guest_info_form['relationship'].data,
                                             gender=guest_info_form['gender'].data,
                                             date_of_birth=guest_info_form['date_of_birth'].data,
                                             phone=guest_info_form['phone'].data,
                                             license_plate=guest_info_form['license_plate'].data)
            new_guest.save()
        except ValueError:
            pass
        return True
    return False
