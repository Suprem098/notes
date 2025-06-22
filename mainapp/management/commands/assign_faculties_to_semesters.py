from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Assign faculties to semesters based on faculty name'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("This command is deprecated as faculty support is removed. No action taken."))
