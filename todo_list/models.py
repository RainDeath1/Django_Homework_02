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

# ДЗ №26


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name= 'Название товара')
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.name
