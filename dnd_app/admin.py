from django.contrib import admin
from .models import Character, Item, ItemType, Weapon, Armor, Consumable, Race

admin.site.register(Character)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'type']

    def display_characters(self, obj):
        return ", ".join([character.name for character in obj.characters.all()])

    display_characters.short_description = "Персонажи"


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'allowed_weight']
