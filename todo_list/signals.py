from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Task, TaskHistory


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print(f"Сигнал активирован для пользователя {instance.username} с 'created'={created}")
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(pre_save, sender=Task)
def log_task_update(sender, instance, **kwargs):
    if instance.pk:  # проверка, что задача уже существует (т.е. это обновление)
        original = Task.objects.get(pk=instance.pk)
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(original, field_name)
            new_value = getattr(instance, field_name)

            if old_value != new_value:
                TaskHistory.objects.create(
                    task=instance,
                    field_name=field_name,
                    old_value=str(old_value),
                    new_value=str(new_value)
                )



