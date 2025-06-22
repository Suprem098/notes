from django.core.management.base import BaseCommand
from mainapp.models import Semester

class Command(BaseCommand):
    help = 'Assign default faculty to existing semesters without faculty'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("This command is deprecated as faculty support is removed. No action taken."))
