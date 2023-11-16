from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Character
from .forms import CharacterForm
from django.shortcuts import get_object_or_404


def index(request):
    characters = Character.objects.all()
    return render(request, 'layout/index.html', {'characters': characters})


def create_character(request):
    if request.method == "POST":
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            character = form.save(commit=False)  
            character.user = request.user
            character.save()
            return redirect('character_details', character_id=character.id)
    else:
        form = CharacterForm()

    return render(request, 'characters/create_character.html', {'form': form})




def character_details(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    return render(request, 'characters/character_detail.html', {'character': character})

