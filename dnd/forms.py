from django import forms
from .models import Character
from django.utils.translation import gettext_lazy as _
from .models import AdvUser


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'character_class', 'race', 'level', 'image', 'strength', 'dexterity', 'constitution',
                  'intelligence', 'wisdom', 'charisma', 'armor_class']


class AdvUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_('Введите пароль'))
    password2 = forms.CharField(label=_('Подтверждение пароля'), widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'bio', 'avatar', 'favorite_race', 'favorite_class', 'experience_level', 'is_dm')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
            'favorite_race': forms.TextInput(attrs={'class': 'form-control'}),
            'favorite_class': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_level': forms.Select(attrs={'class': 'form-control'}),
            'is_dm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_('Пароли не совпадают.'))
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


