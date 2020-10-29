from django import forms
from datetime import datetime, timedelta

from registration.definition import ServeState
from booking.definition import Use
from booking.models import Guest


class BookingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try:
            applicant = kwargs.pop('applicant')
        except KeyError:
            applicant = None
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['unit_of_applicant'] = forms.CharField(required=True,
                                                           max_length=50,
                                                           widget=forms.TextInput(attrs={'class': 'form-control'}))
        if applicant.officer:
            if applicant.officer.serve_state == ServeState.Active.value[0]:
                self.fields['unit_of_applicant'].initial = applicant.officer.branch.name
            else:
                self.fields['unit_of_applicant'].initial = "Retirement"

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


class GuestInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.booking_source = kwargs.pop('booking_source')
        super(GuestInfoForm, self).__init__(*args, **kwargs)

    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    ID_Number = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    rank = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    relationship = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    GENDER_CHOICES = [('', 'Select your gender'), (1, 'Male'), (2, 'Female')]
    gender = forms.ChoiceField(required=False,
                               choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'YYYY-MM-DD'}))
    phone = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    license_plate = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Guest
        fields = ['name', 'ID_Number', 'rank', 'relationship', 'gender', 'date_of_birth', 'phone', 'license_plate']
