# Generated by Django 4.2.2 on 2023-10-05 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0018_alter_documents_file_alter_documents_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='file',
            field=models.FileField(upload_to='documents/files', verbose_name='Файл'),
        ),
    ]