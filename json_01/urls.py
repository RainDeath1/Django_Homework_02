from django.urls import path
from json_01.views import fetch_todos

urlpatterns = [
    path('fetch_todos/', fetch_todos),
]

