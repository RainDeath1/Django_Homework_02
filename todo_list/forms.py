from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from .models import Task, IceCream, Product


# class TaskForm(forms.ModelForm):
#     due_date = forms.DateField(
#         widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
#         input_formats=('%Y-%m-%d', )
#     )
# home_27


class TaskForm(forms.ModelForm):
    title = forms.CharField(label="Название задачи", max_length=50)
    description = forms.CharField(label="Описание", widget=forms.widgets.Textarea())
    due_date = forms.DateField(
        widget=forms.DateInput(format= '%Y-%m-%d', attrs={'type':'date'}),
        input_formats=('%Y-%m-%d',),
        label='Дата выполнения'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) <= 3:
            raise ValidationError("Название задачи должно содержать более 3 символов!")
        return title


TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=3)


class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ['name', 'description', 'price', 'flavor']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'placeholder': 'Описание'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Цена'}),
            'flavor': forms.TextInput(attrs={'placeholder': 'Вкус мороженного'}),
        }

#26


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
