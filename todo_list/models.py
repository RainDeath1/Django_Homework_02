from django.db import models
from django.contrib.auth.models import User
from precise_bbcode.bbcode import get_parser

from kzflavor.models import KZIINField, KZIDCardField
from precise_bbcode.fields import BBCodeTextField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    due_date = models.DateField(verbose_name='Дата выполнения')
    #37
    file = models.FileField(upload_to='tasks_files/', null=True, blank=True, verbose_name='Загрузка файла')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


#home_42
class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history")
    field_name = models.CharField(max_length=100, verbose_name="Название поля")
    old_value = models.TextField(null=True, blank=True, verbose_name='Старое значение поля')
    new_value = models.TextField(null=True, blank=True, verbose_name='Новое значение поля')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'История изменений'


class Change(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()


class IceCream(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название мороженного')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена')
    flavor = models.CharField(max_length=50, verbose_name='Вкус')

    def __str__(self):
        return self.name


#31

class ProductQuerySet(models.QuerySet):
    def in_price_range(self, min_price, max_price):
        return self.filter(price__gte=min_price, price__lte=max_price)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def in_price_range(self, min_price, max_price):
        return self.get_queryset().in_price_range(min_price, max_price)
# ДЗ №26


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name= 'Название товара')
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/image', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    artist = models.CharField(max_length=100, verbose_name='Исполнитель')

    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    songs = models.ManyToManyField(Song, related_name='playlist', verbose_name='Песни')

    def __str__(self):
        return self.name


#home_30
class DiscountableProduct(Product):
    discount_percent = models.PositiveSmallIntegerField(default=0, verbose_name="Процент скидки")

    class Meta:
        abstract = True

    def discounted_price(self):
        return self.price * (100 - self.discount_percent) / 100


class PremiumProduct(DiscountableProduct):
    is_limited_edition = models.BooleanField(default=False, verbose_name="Ограниченное издание")
    premium_packaging = models.BooleanField(default=False, verbose_name="Премиальная упаковка")

    def __str__(self):
        return f"Премиум: {self.name}"


#32
class FeedbackMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField()
    message = models.TextField(verbose_name="описание")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    iin = KZIINField(verbose_name="ИИН")
    id_card = KZIDCardField(verbose_name="Номер удостоверения")


class Sending(models.Model):
    content = BBCodeTextField()
    rendered_content = models.TextField(editable=False, blank=True)

    def save(self, *args, **kwargs):
        bbcode_parser = get_parser()
        self.rendered_content = bbcode_parser.render(str(self.content))
        super().save(*args, **kwargs)


class Documents(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название документа')
    file = models.FileField(upload_to='documents/files', verbose_name='Файл')
    image = models.ImageField(upload_to='documents/images', blank=True, null=True)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(100, 50)],
                               format='JPEG', options={'quality': 60})

#home_42
# class Article(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#
#
# class ArticleHistory(models.Model):
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     updated_at = models.DateTimeField(auto_now_add=True)
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE)


# home_45_start
class AddressBook(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField()
    phone_number = models.CharField(max_length=50, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Записная книжка'
