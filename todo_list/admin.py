from django.contrib import admin
from .models import Task, Change, Song, Playlist, Sending, Product, Documents, TaskHistory

admin.site.register(Task)
admin.site.register(Change)
admin.site.register(Product)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ['content']


@admin.register(Documents)
class DocumentAdmin(admin.ModelAdmin):
    localflavor = ['title', 'file']


@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ['task', 'field_name', 'old_value', 'new_value', 'updated_at']
    readonly_fields = ['task', 'field_name', 'old_value', 'new_value', 'updated_at']
