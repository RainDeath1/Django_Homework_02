# scripts.py
from django.contrib.auth.models import User
from todo_list.models import Profile  # Укажите имя вашего приложения


def create_profiles_for_existing_users():
    users_without_profile = User.objects.filter(profile=None)
    for user in users_without_profile:
        Profile.objects.create(user=user)
