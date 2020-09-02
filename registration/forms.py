from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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


class AccountChangeForm(UserChangeForm):
    first_name = forms.CharField(required=True,
                                 max_length=150,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True,
                                max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    GENDER_CHOICES = [(_.value[0], _.value[1]) for _ in Gender.__members__.values()]
    gender = forms.ChoiceField(required=True,
                               choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=True,
                                   max_length=15,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(required=True,
                               help_text="Your birthday input format: 'yyyy-mm-dd'.",
                               error_messages={'invalid': "Maybe the format is wrong, please check it again."},
                               widget=forms.DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'phone_number', 'birthday']
