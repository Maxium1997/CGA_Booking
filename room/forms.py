from django import forms

from registration.models import User
from registration.definition import Identity
from room.models import Hotel, Room, Dormitory


class HotelForm(forms.ModelForm):
    external_appearance = forms.ImageField()
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Please enter the English name of your hotel.'}))
    address = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'type': 'number'}))
    website = forms.URLField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'type': 'url'}))
    introduction = forms.CharField(required=False,
                                   widget=forms.Textarea(attrs={'rows': 10,
                                                                'cols': 50,
                                                                'class': 'form-control',
                                                                'placeholder': 'Please write something to describe your hotel.'}))

    class Meta:
        model = Hotel
        fields = ['external_appearance', 'name', 'slug', 'address', 'phone', 'website', 'introduction']


class HotelTransferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            hotel = kwargs.pop('hotel')
        except KeyError:
            hotel = None
        super(HotelTransferForm, self).__init__(*args, **kwargs)
        self.fields['owner'] = forms.ModelChoiceField(required=True,
                                                      queryset=User.objects.filter(identity=Identity.Proprietor.value[0]),
                                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                                      initial=hotel.owner)

    class Meta:
        model = Hotel
        fields = ['owner']


class RoomForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'type': 'number',
                                                          'placeholder:': 'If you don\'t want to set, please enter 0.'}))
    single_bed = forms.IntegerField(required=True,
                                    widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                    'type': 'number'}))
    double_bed = forms.IntegerField(required=True,
                                    widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                    'type': 'number'}))
    size = forms.CharField(required=True,
                           widget=forms.NumberInput(attrs={'class': 'form-control',
                                                           'type': 'number',
                                                           'placeholder:': 'If you don\'t want to set, please enter 0.'}))

    class Meta:
        model = Room
        fields = ['name', 'price', 'single_bed', 'double_bed', 'size']


class DormitorySettingForm(forms.ModelForm):
    washing_fee = forms.IntegerField(required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                     'type': 'number'}))
    usage_fee = forms.IntegerField(required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                   'type': 'number'}))
    utility_bill = forms.IntegerField(required=False,
                                      widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                      'type': 'number'}))

    class Meta:
        model = Dormitory
        fields = ['washing_fee', 'usage_fee', 'utility_bill']
