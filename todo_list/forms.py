from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        input_formats=('%Y-%m-%d', )
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
