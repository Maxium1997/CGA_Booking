from django import forms
from django.utils.text import slugify

from rank.models import Service, Branch


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


class BranchForm(ServiceForm):
    class Meta:
        model = Branch
        fields = ['name', 'slug']

    def save(self, commit=True):
        branch = super().save(commit=False)
        branch.slug = slugify(self.cleaned_data['slug'])
        if commit:
            branch.save()
        return branch
