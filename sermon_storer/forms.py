from django import forms
from .models import Sermon

class FTPPasswordForm(forms.Form):
    sermon_select = forms.ModelMultipleChoiceField(
        queryset=Sermon.objects.all().order_by('-date')[:20],
        widget=forms.CheckboxSelectMultiple()
    )
