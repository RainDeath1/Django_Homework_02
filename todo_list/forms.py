from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from .models import Task, IceCream, Product, Playlist, Song, Profile, Sending, Documents
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        fields = ['title', 'description', 'due_date', 'file']

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
        fields = ['name', 'description', 'price', 'image']


#29
class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'songs']


class SongForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите код с картинки', error_messages={'invalid':'Неправильный код'})

    class Meta:
        model = Song
        fields = ['title', 'artist']

#home_32
class FeedbackForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100)
    email = forms.EmailField(label="Ваш e-mail")
    message = forms.CharField(label="Сообщение", widget=forms.Textarea)


#home_33
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'iin', 'id_card']


class SendingForm(forms.ModelForm):
    class Meta:
        model = Sending
        fields = ['content']


#home_38
class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['title', 'file', 'image']


#home_39
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]