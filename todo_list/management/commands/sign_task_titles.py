from django.core.management.base import BaseCommand
from django.core.signing import Signer
from todo_list.models import Task


class Command(BaseCommand):
    help = 'Подпись задач в базе данных'

    def handle(self, *args, **options):
        signer = Signer()
        tasks = Task.objects.all()

        for task in tasks:
            signed_title = signer.sign(task.title)
            task.title = signed_title
            task.save()

        self.stdout.write(self.style.SUCCESS('Все задачи успешно подписаны'))
