from django.core.management.base import BaseCommand
from mainapp.models import Faculty

class Command(BaseCommand):
    help = 'Print all faculties, semesters, and subjects for debugging'

    def handle(self, *args, **kwargs):
        faculties = Faculty.objects.all()
        if not faculties:
            self.stdout.write("No faculties found.")
            return

        for faculty in faculties:
            self.stdout.write(f"Faculty: {faculty.name} (slug: {faculty.slug})")
            semesters = faculty.semesters.all()
            if not semesters:
                self.stdout.write("  No semesters found for this faculty.")
                continue
            for semester in semesters:
                self.stdout.write(f"  Semester: {semester.name}")
                subjects = semester.subjects.all()
                if not subjects:
                    self.stdout.write("    No subjects found for this semester.")
                    continue
                for subject in subjects:
                    self.stdout.write(f"    Subject: {subject.name}")
