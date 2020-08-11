from django import forms
from django.contrib.auth.forms import UserCreationForm

from registration.models import User
from registration.definition import Privilege, Identity, Gender


class TravelerRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ID_Number = forms.CharField(required=True,
                                max_length=20,
                                widget=forms.TextInput(attrs={'id': 'id_number',
                                                              'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password',
                                                              'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password',
                                                              'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'ID_Number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.privilege = Privilege.User.value[0]
        user.identity = Identity.Traveler.value[0]
        user.gender = Gender.Unset.value[0]
        if commit:
            user.save()
        return user


class ProprietorRegisterForm(TravelerRegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.privilege = Privilege.User.value[0]
        user.identity = Identity.Proprietor.value[0]
        user.gender = Gender.Unset.value[0]
        if commit:
            user.save()
        return user
