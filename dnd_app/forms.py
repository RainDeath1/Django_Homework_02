from django import forms
from .models import Character, Item


class CharacterForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Character
        fields = ['name', 'race', 'character_class', 'level', 'image', 'items']
