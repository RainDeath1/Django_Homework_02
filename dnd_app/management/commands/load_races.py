from django.core.management.base import BaseCommand
from dnd_app.models import Race


class Command(BaseCommand):
    help = 'Load races into the database'

    def handle(self, *args, **kwargs):
        self.populate_races()

    def populate_races(self):
        races_data = [
            {"name": "Человек", "allowed_weight": 120},
            {"name": "Эльф", "allowed_weight": 100},
            {"name": "Дварф", "allowed_weight": 150},
            {"name": "Полурослик", "allowed_weight": 80},
            {"name": "Орк", "allowed_weight": 140},
        ]

        for race_data in races_data:
            Race.objects.create(**race_data)

        self.stdout.write(self.style.SUCCESS('All races loaded!'))
