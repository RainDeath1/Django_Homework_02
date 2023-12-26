from django.urls import path
from .views import (index, CreateUserView, LogoutView, LoginView, user_profile,
                    UserCharacterView, EditProfileView, create_character)

app_name = 'dnd'

urlpatterns = [
    path('', index, name='index'),
    path('register/',  CreateUserView.as_view(), name='user_register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('user_profile/', user_profile, name='user_profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('user_character/', UserCharacterView.as_view(), name='user_characters'),
    path('create_character', create_character, name='create')

]
