from django import forms
from django.utils.text import slugify

from rank.models import Service, Branch, MilitaryService, MilitaryBranch, Rank


class ServiceForm(forms.ModelForm):
    name = forms.CharField(required=True)
    slug = forms.SlugField(required=True)

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
    class Meta:
        model = Rank
        fields = ['equivalent_NATO_code', 'name', 'slug']
