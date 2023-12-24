from django import forms
from core import models

class ProfessorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].help_text = None
            self.fields[name].widget.attrs.update({
                'class': 'form-control mb-3',
                'autocomplete': 'off'
            })

    class Meta:
        model = models.Professor
        fields = [
            'first_name',
            'last_name',
            # 'minimum_units',
            # 'maximum_units',
        ]