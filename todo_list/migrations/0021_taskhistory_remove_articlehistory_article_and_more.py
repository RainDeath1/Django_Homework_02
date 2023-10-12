# Generated by Django 4.2.2 on 2023-10-12 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0020_article_articlehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('old_value', models.TextField(blank=True, null=True)),
                ('new_value', models.TextField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='todo_list.task')),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.RemoveField(
            model_name='articlehistory',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articlehistory',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='ArticleHistory',
        ),
    ]