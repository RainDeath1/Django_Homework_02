# Generated by Django 4.2.2 on 2023-10-12 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0023_alter_taskhistory_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]
