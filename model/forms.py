from django import forms
from .models import IceCream

class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ['flavor', 'price', 'manufacturer', 'calories', 'description', 'image']

    def clean_calories(self):
        calories = self.cleaned_data.get('calories')

        if calories < 0:
            raise forms.ValidationError("Количество калорий не может быть отрицательным.")

        return calories
