from django import forms
from core import models

class CurriculumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].help_text = None
            self.fields[name].widget.attrs.update({
                'class': 'form-control mb-3',
                'autocomplete': 'off'
            })
        self.fields['course'].queryset = models.Course.objects.filter(department=department)
        self.fields['course'].label_from_instance = lambda obj: obj.name

    class Meta:
        model = models.Curriculum
        fields = [
            'name',
            'course',
        ]