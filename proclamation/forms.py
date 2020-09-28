from django import forms
from django.core.exceptions import PermissionDenied

from registration.models import User
from proclamation.models import Proclamation


class ProclamationForm(forms.ModelForm):
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(required=True,
                              widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Proclamation
        fields = ['title', 'content', 'is_public']

    def save(self, commit=True, recipient: User = None, announcer: User = None):
        obj = super(ProclamationForm, self).save(commit=False)
        if self.cleaned_data['is_public']:
            obj.created_by = announcer
            obj.save()
        return obj
