from django import forms
from django.utils.text import slugify

from rank.models import Service, Branch, MilitaryService, MilitaryBranch, Rank


class ServiceForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.SlugField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Service
        fields = ['name', 'slug']

    def save(self, commit=True):
        service = super().save(commit=False)
        service.slug = slugify(self.cleaned_data['slug'])
        if commit:
            service.save()
        return service


class MilitaryServiceForm(ServiceForm):
    class Meta:
        model = MilitaryService
        fields = ['name', 'slug']


class BranchForm(ServiceForm):
    class Meta:
        model = Branch
        fields = ['name', 'slug']


class MilitaryBranchForm(ServiceForm):
    class Meta:
        model = MilitaryBranch
        fields = ['name', 'slug']


class RankForm(ServiceForm):
    class Meta:
        model = Rank
        fields = ['name', 'slug']
