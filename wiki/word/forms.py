from django import forms

from word.models import WikiWord


class WikiWordForm(forms.ModelForm):
    class Meta:
        model = WikiWord
        fields = (
            'text',
        )
