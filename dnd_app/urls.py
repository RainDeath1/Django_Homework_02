from django.urls import path

from .views import index,create_character, character_details

urlpatterns = [
    path('', index, name='index'),
    path('create_character/', create_character, name='create_character'),
    path('character/<int:character_id>/', character_details, name='character_details'),
]

