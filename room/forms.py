from django import forms

from room.models import Hotel


class HotelCreationForm(forms.ModelForm):
    external_appearance = forms.ImageField()
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Please enter the English name of your hotel.'}))
    address = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    website = forms.URLField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    introduction = forms.CharField(required=False,
                                   widget=forms.Textarea(attrs={'rows': 10,
                                                                'cols': 50,
                                                                'class': 'form-control',
                                                                'placeholder': 'Please write something to describe your hotel.'}))

    class Meta:
        model = Hotel
        fields = ['external_appearance', 'name', 'slug', 'address', 'phone', 'website', 'introduction']