from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError


def get_min_length():
    min_length = 3
    return min_length

def validator_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечетное',code='odd', params={'value': val} )



class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введённое число должно быть > %(min)s '
                                  'и < %(max)s',
                                  code='out_of_range',
                                  params={'min': self.min_value,
                                          'max': self.max_value})


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class Spare(models.Model):
    name = models.CharField(max_length=30)

class Machine(models.Model):
    name = models.CharField(max_length=30)
    spare = models.ManyToManyField(Spare)


class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name = 'Название'
    )

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self):
        if True:
            super().save(*args,*kwargs)

    def delete(self):
        # Выполняем какие-то действия до удаления
        if True:
            super().delete(*args, *kwargs)
        # Выполняем какие-то действия после удаления

    def get_absolute_url(self):
        # return "/bboard/%s/" % self.pk
        # return f"/bboard/{self.pk}/"
        return f"/{self.pk}/"




class Bb(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
        validators= [validators.MinLengthValidator(get_min_length())],
        # validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'min_length': 'Слишком мало символов'}

    )

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание ' 'продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите ' 'неотрицательное значение цены')
        if errors: raise ValidationError(errors)

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )

    price = models.FloatField(
        null=True,
        blank=True,
        validators=[validator_even, MinMaxValueValidator(50,60_000_000)],
        verbose_name='Цена',
         )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )

    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    class Meta:
        verbose_name_plural = "Объявления"
        verbose_name = "Объявление"
        ordering = ['-published']

    def title_and_price(self):
        if self.price:
            # return '%s (%.2f)' % (self.title, self.price)
            return f'{self.title} ({self.price:.2f})'
        return self.title