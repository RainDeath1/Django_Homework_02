from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    due_date = models.DateField(verbose_name='Дата выполнения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


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
