from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from registration.models import User, Officer, Experience, Education, Work
from registration.definition import Privilege, Identity, Gender, ServeState, MilitaryServiceState

from rank.models import Service, Branch, MilitaryService, MilitaryBranch, Rank


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
                               widget=forms.DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'phone_number', 'birthday']


class OfficerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            service = kwargs.pop('service')
            military_service = kwargs.pop('military_service')
        except KeyError:
            service = None
            military_service = None
        super(OfficerForm, self).__init__(*args, **kwargs)
        self.fields['service'] = forms.ModelChoiceField(required=False,
                                                        queryset=Service.objects.all(),
                                                        widget=forms.Select(attrs={'onchange': 'submit()'}))
        self.fields['branch'] = forms.ModelChoiceField(required=False,
                                                       queryset=Branch.objects.filter(service=service))
        self.fields['military_service'] = forms.ModelChoiceField(required=False,
                                                                 queryset=MilitaryService.objects.all(),
                                                                 widget=forms.Select(attrs={'onchange': 'submit()'}))
        self.fields['military_branch'] = forms.ModelChoiceField(required=False,
                                                                queryset=MilitaryBranch.objects.filter(military_service=military_service))
        self.fields['rank'] = forms.ModelChoiceField(required=False,
                                                     queryset=Rank.objects.filter(military_service=military_service))

    SERVE_STATE = [('0', 'Select your serve state')] + [(str(_.value[0]), _.value[1]) for _ in ServeState.__members__.values()]
    serve_state = forms.ChoiceField(required=True,
                                    choices=SERVE_STATE,
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    MILITARY_SERVICE_STATE = [('0', 'Select your military service')] + [(str(_.value[0]), _.value[1]) for _ in MilitaryServiceState.__members__.values()]
    military_service_state = forms.ChoiceField(required=True,
                                               choices=MILITARY_SERVICE_STATE,
                                               widget=forms.Select(attrs={'class': 'form-control'}))
    level = forms.IntegerField(required=False,
                               widget=forms.NumberInput(attrs={'style': 'width: 20%'}))
    date_of_enlist = forms.DateField(required=False,
                                     widget=forms.DateInput(attrs={'class': 'form-control'}),
                                     help_text="Date Format: YYYY-MM-DD")
    date_of_retire = forms.DateField(required=False,
                                     widget=forms.DateInput(attrs={'class': 'form-control'}),
                                     help_text="<i style=\"color: red;\">Date Format: YYYY-MM-DD</i>")

    class Meta:
        model = Officer
        exclude = ['user',
                   'attachment_of_military_ID_card_front', 'attachment_of_military_ID_card_back',
                   'attachment_of_badge_front', 'attachment_of_badge_back',
                   'identity_authentication', 'serve_record']


class AttachmentForm(forms.Form):
    attachment = forms.ImageField(required=False)


class ExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            user = kwargs.pop('user')
        except KeyError:
            user = None
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['finished_date'].required = False


class EducationForm(ExperienceForm):
    class Meta:
        model = Education
        fields = ['class_name', 'started_date', 'finished_date']


class WorkForm(ExperienceForm):
    class Meta:
        model = Work
        fields = ['position', 'started_date', 'finished_date']
