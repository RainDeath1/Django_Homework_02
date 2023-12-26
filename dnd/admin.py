from django.contrib import admin
from .models import Race, Character, ItemType, Weapon, Armor, Consumable, ItemAttribute, AdvUser


admin.site.register(Race)
admin.site.register(ItemType)
admin.site.register(Weapon)
admin.site.register(Armor)
admin.site.register(Consumable)
admin.site.register(ItemAttribute)


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'race', 'character_class', 'level')
    search_fields = ('name', 'race__name', 'character_class')
    list_filter = ('race', 'character_class', 'level')


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'favorite_race', 'is_active', 'is_staff')
    search_fields = ('username', 'email')


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Character, CharacterAdmin)
