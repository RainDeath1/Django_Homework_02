from django.contrib import admin
from .models import Task, Change, Song, Playlist

admin.site.register(Task)
admin.site.register(Change)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name']
