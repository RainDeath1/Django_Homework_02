from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

class Child(models.Model):
    parent = models.ForeignKey(Person, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

class IceCream(models.Model):
    FLAVORS = [
        ('CH', 'Chocolate'),
        ('VA', 'Vanilla'),
        ('ST', 'Strawberry'),
        ('CA', 'Caramel'),
        ('CO', 'Coconut'),
        ('PI', 'Pistachio'),
        ('MI', 'Mint'),
    ]
    flavor = models.CharField(max_length=2, choices=FLAVORS)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    manufacturer = models.CharField(max_length=100)
    calories = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='ice_creams/', blank=True, null=True)

class IceCreamKiosk(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    ice_creams = models.ManyToManyField(IceCream)