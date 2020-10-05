from django import forms
from django.utils.text import slugify

from rank.models import Service, Branch, MilitaryService, MilitaryBranch, Rank


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control badge-pill'}))
        self.fields['slug'] = forms.CharField(required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control badge-pill'}))

    class Meta:
        model = Service
        fields = ['name', 'slug']

    def save(self, commit=True):
        self_object = super().save(commit=False)
        self_object.slug = slugify(self.cleaned_data['slug'].strip())
        if commit:
            self_object.save()
        return self_object


class BranchForm(ServiceForm):
    class Meta:
        model = Branch
        fields = ['name', 'slug']


class MilitaryServiceForm(ServiceForm):
    class Meta:
        model = MilitaryService
        fields = ['name', 'slug']


class MilitaryBranchForm(ServiceForm):
    class Meta:
        model = MilitaryBranch
        fields = ['name', 'slug']


class RankForm(ServiceForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['equivalent_NATO_code'] = forms.CharField(required=True,
                                                              widget=forms.TextInput(attrs={'class': 'form-control badge-pill'}))
        self.fields['name'] = forms.CharField(required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control badge-pill'}))
        self.fields['slug'] = forms.CharField(required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control badge-pill'}))

    class Meta:
        model = Rank
        fields = ['equivalent_NATO_code', 'name', 'slug']
