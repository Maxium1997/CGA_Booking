from django import forms
from datetime import datetime, timedelta

from booking.models import Booking, Guest
from booking.definition import Use


class BookingForm(forms.Form):
    unit_of_applicant = forms.CharField(required=True,
                                        max_length=50,
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))

    USE_CHOICES = [('', 'Select your use')] + [(str(_.value[0]), _.value[1]) for _ in Use.__members__.values()]
    use = forms.ChoiceField(required=True,
                            choices=USE_CHOICES,
                            widget=forms.Select(attrs={'class': 'form-control'}))

    DATE_CHOICES = [('', 'Select your check in time')]
    now_date = datetime.now().strftime('%Y-%m-%d')
    for i in range(60):
        now_date = datetime.strptime(now_date, '%Y-%m-%d')
        now_date = now_date + timedelta(days=1)
        now_date = now_date.strftime('%Y-%m-%d')
        DATE_CHOICES.append((now_date, now_date))
    check_in_time = forms.ChoiceField(required=False,
                                      choices=DATE_CHOICES,
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    days = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['unit_of_applicant', 'use', 'check_in_time', 'days']


class GuestInfoForm(forms.Form):
    name = forms.CharField(required=False,
                           widget=forms.TextInput)
    ID_Number = forms.CharField(required=False,
                                widget=forms.TextInput)
    rank = forms.CharField(required=False,
                           widget=forms.TextInput)
    relationship = forms.CharField(required=False,
                                   widget=forms.TextInput)

    GENDER_CHOICES = [('', 'Select your gender'), (1, 'Male'), (2, 'Female')]
    gender = forms.ChoiceField(required=False,
                               choices=GENDER_CHOICES,
                               widget=forms.Select)
    date_of_birth = forms.DateField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
                                    help_text="<br><i style=\"color: red\">This column data format: YYYY-MM-DD</i>")
    phone = forms.CharField(required=False,
                            widget=forms.TextInput)
    license_plate = forms.CharField(required=False,
                                    widget=forms.TextInput)

    class Meta:
        fields = ['name', 'ID_Number', 'rank', 'relationship', 'gender', 'date_of_birth', 'phone', 'license_plate']
