from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel


class AdvUser(AbstractUser):
    EXPERIENCE_CHOICES= (
        ("beginner", _("Новичок")),
        ("intermediate", _("Средний")),
        ("advanced", _("Опытный")),
        ("expert", _("Эксперт"))
    )
    bio = models.TextField(_("Биография"), blank=True)
    avatar = models.ImageField(_("Аватар"), upload_to='media/user_avatars/', blank=True, null=True)
    favorite_race = models.CharField(_("Любимая раса"), max_length=50, blank=True, null=True)
    favorite_class = models.CharField(_("Любимый класс"), max_length=50, blank=True, null=True)
    experience_level = models.CharField(_("Уровень опыта"), max_length=50, choices=EXPERIENCE_CHOICES,
                                        default='beginner')
    is_dm = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


class Race(models.Model):
    name = models.CharField(max_length=50, verbose_name='Раса')
    allowed_weight = models.PositiveIntegerField(verbose_name="Допустимый вес")
    characteristics = models.TextField(blank=True, null=True, verbose_name="Особенности")
    history = models.TextField(blank=True, null=True, verbose_name="История расы")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Раса'
        verbose_name_plural = 'Расы'


class Character(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Имя')
    character_class = models.CharField(max_length=50, verbose_name="Класс")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name='Раса')
    level = models.PositiveIntegerField(default=1, verbose_name='Уровень персонажа')
    image = models.ImageField(upload_to='media/character_images', blank=True, null=True, verbose_name='Фото персонажа')
    strength = models.IntegerField(verbose_name='Сила', default=0)
    dexterity = models.IntegerField(verbose_name='Ловкость', default=0)
    constitution = models.IntegerField(verbose_name='Телосложение', default=0)
    intelligence = models.IntegerField(verbose_name='Интеллект', default=0)
    wisdom = models.IntegerField(verbose_name='Мудрость', default=0)
    charisma = models.IntegerField(verbose_name='Харизма', default=0)
    strength_modifier = models.IntegerField(verbose_name='Модификатор Силы', default=0)
    dexterity_modifier = models.IntegerField(verbose_name='Модификатор Ловкости', default=0)
    constitution_modifier = models.IntegerField(verbose_name='Модификатор Телосложения', default=0)
    intelligence_modifier = models.IntegerField(verbose_name='Модификатор Интеллекта', default=0)
    wisdom_modifier = models.IntegerField(verbose_name='Модификатор Мудрости', default=0)
    charisma_modifier = models.IntegerField(verbose_name='Модификатор Харизмы', default=0)
    armor_class = models.IntegerField(default=10, verbose_name='Класс брони')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'


class ItemType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип предмета")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип предмета'
        verbose_name_plural = 'Типы предметов'


class MaterialProperties(models.Model):
    material = models.CharField(max_length=50, blank=True, null=True, verbose_name="Материал")
    weight = models.FloatField(blank=True, null=True, verbose_name="Вес")

    class Meta:
        abstract = True


class AbstractItem(PolymorphicModel):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, verbose_name='Тип предмета')
    characters = models.ManyToManyField(Character, related_name='items', verbose_name="Персонажи")

    def __str__(self):
        return self.name


class Weapon(AbstractItem, MaterialProperties):
    WEAPON_CHOICES = (
        ('MELEE', 'Ближний бой'),
        ('RANGED', 'Дальний бой'),
        ('MAGIC', 'Магическое'),
        ('OTHER', 'Другое'),
    )

    weapon_type = models.CharField(max_length=50, choices=WEAPON_CHOICES, default='OTHER', verbose_name="Тип оружия")
    damage = models.PositiveIntegerField(blank=True, null=True, verbose_name="Урон")

    class Meta:
        verbose_name_plural = 'Оружие'


class Armor(AbstractItem, MaterialProperties):
    ARMOR_CHOICES = (
        ('HEAVY', 'Тяжелый'),
        ('MEDIUM', 'Средний'),
        ('LIGHT', 'Легкий'),
        ('SHIELD', 'Щит'),
    )

    armor_type = models.CharField(max_length=50, choices=ARMOR_CHOICES, default='LIGHT', verbose_name="Тип доспеха")
    defense = models.PositiveIntegerField(blank=True, null=True, verbose_name="Защита")

    @property
    def armor_class(self):
        return self.ARMOR_CLASS_BASE.get(self.armor_type, 10) + self.defense_modifier

    class Meta:
        verbose_name = 'Броня'
        verbose_name_plural = 'Броня'


class Consumable(AbstractItem):
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


class ItemAttribute(models.Model):
    item = models.ForeignKey(AbstractItem, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, verbose_name="Ключ атрибута")
    value = models.CharField(max_length=250, verbose_name="Значение атрибута")

    class Meta:
        unique_together = ['item', 'key']
        verbose_name = 'Свойства предмета'
        verbose_name_plural = 'Свойства предметов'

    def __str__(self):
        return f"{self.key}: {self.value}"


class Currency(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='currencies')
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f"{self.amount} {self.name} у {self.character.name}"

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
