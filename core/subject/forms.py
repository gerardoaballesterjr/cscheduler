from django import forms
from core import models

class SubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].help_text = None
            self.fields[name].widget.attrs.update({
                'class': 'form-control mb-3',
                'autocomplete': 'off'
            })
        self.fields['room_type'].queryset = models.RoomType.objects.filter(models.models.Q(department=department) | models.models.Q(department=None))
        self.fields['room_type'].label_from_instance = lambda obj: obj.name
        self.fields['curriculum'].queryset = models.Curriculum.objects.filter(department=department)
        self.fields['curriculum'].label_from_instance = lambda obj: obj.name

    class Meta:
        model = models.Subject
        fields = [
            'name',
            'code',
            'type',
            'units',
            'hours',
            'level',
            'curriculum',
            'room_type',
        ]