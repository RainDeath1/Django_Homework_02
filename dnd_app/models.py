from django.db import models
from django.contrib.auth.models import User


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Имя')
    character_class = models.CharField(max_length=50, verbose_name='Класс персонажа')
    race = models.CharField(max_length=50, verbose_name='Раса')
    level = models.PositiveIntegerField(default=1, verbose_name='Уровень')
    image = models.ImageField(upload_to='character_images/', blank=True, null=True, verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"


class ItemType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип предмета")

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, verbose_name='Тип предмета')
    characters = models.ManyToManyField(Character, related_name='items', verbose_name="Персонажи")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Weapon(Item):
    WEAPON_CHOICES = (
        ('MELEE', 'Ближний бой'),
        ('RANGED', 'Дальний бой'),
        ('MAGIC', 'Магическое'),
        ('OTHER', 'Другое'),
    )

    weapon_type = models.CharField(max_length=50, choices=WEAPON_CHOICES, default='OTHER', verbose_name="Тип оружия")
    damage = models.PositiveIntegerField(blank=True, null=True, verbose_name="Урон")
    material = models.CharField(max_length=50, blank=True, null=True, verbose_name="Материал")
    weight = models.FloatField(blank=True, null=True, verbose_name="Вес")


class ItemAttribute(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, verbose_name="Ключ атрибута")
    value = models.CharField(max_length=250, verbose_name="Значение атрибута")

    class Meta:
        unique_together = ['item', 'key']


class Armor(Item):
    ARMOR_CHOICES = (
        ('HEAVY', 'Тяжелый'),
        ('MEDIUM', 'Средний'),
        ('LIGHT', 'Легкий'),
        ('SHIELD', 'Щит'),
    )

    armor_type = models.CharField(max_length=50, choices=ARMOR_CHOICES, default='MEDIUM', verbose_name="Тип доспеха")
    defense = models.PositiveIntegerField(blank=True, null=True, verbose_name="Защита")
    material = models.CharField(max_length=50, blank=True, null=True, verbose_name="Материал")
    weight = models.FloatField(blank=True, null=True, verbose_name="Вес")


class Consumable(Item):
    EFFECT_CHOICES = (
        ('HEAL', 'Лечение'),
        ('BUFF', 'Усиление'),
        ('DEBUFF', 'Ослабление'),
        ('OTHER', 'Другое'),
    )

    effect_type = models.CharField(max_length=50, choices=EFFECT_CHOICES, default='OTHER', verbose_name="Тип эффекта")
    effect_strength = models.PositiveIntegerField(verbose_name="Сила эффекта", null=True, blank=True)
    duration = models.DurationField(blank=True, null=True, verbose_name="Продолжительность действия")

    class Meta:
        verbose_name_plural = 'Расходники'


class Currency(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f"{self.amount} {self.name} у {self.character.name}"

