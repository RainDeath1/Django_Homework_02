from django.contrib import admin
from .models import Task, Change, Song, Playlist, Sending, Product, Documents, TaskHistory, AddressBook, Profile

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


class AddressBookAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ['name', 'email', 'phone_number']
    list_filter = ['name', 'email']
    list_editable = ['email', 'phone_number']
    list_display_links = ['name']


admin.site.register(AddressBook, AddressBookAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'iin', 'id_card')
    search_fields = ('user__username', 'phone_number', 'iin', 'id_card')
    list_filter = ('user',)


admin.site.register(Profile, ProfileAdmin)
