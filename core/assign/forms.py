from django import forms
from core import models

class AssignForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].help_text = None
            self.fields[name].widget.attrs.update({
                'class': 'form-control mb-3',
                'autocomplete': 'off'
            })

        self.fields['days'].label_from_instance = lambda obj: obj.name
        self.fields['semester'].label_from_instance = lambda obj: obj.name
        
        self.fields['subject'].queryset = models.Subject.objects.filter(department=department)
        self.fields['subject'].label_from_instance = lambda obj: obj.name
        self.fields['professor'].queryset = models.Professor.objects.filter(department=department)
        self.fields['professor'].label_from_instance = lambda obj: f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = models.Assign
        fields = [
            'days',
            'subject',
            'professor',
            'semester',
        ]