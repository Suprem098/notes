from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Clean invalid faculty foreign keys in Semester table by setting them to NULL or valid faculty'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Check if faculty_id column exists
            cursor.execute("PRAGMA table_info(mainapp_semester);")
            columns = [row[1] for row in cursor.fetchall()]
            if 'faculty_id' not in columns:
                self.stdout.write(self.style.WARNING("Column 'faculty_id' does not exist in 'mainapp_semester'. Nothing to clean."))
                return

            # Set faculty_id to NULL where it does not exist in Faculty table
            cursor.execute("""
                UPDATE mainapp_semester
                SET faculty_id = NULL
                WHERE faculty_id IS NOT NULL
                AND faculty_id NOT IN (SELECT id FROM mainapp_faculty)
            """)
        self.stdout.write(self.style.SUCCESS("Cleaned invalid faculty foreign keys in Semester table."))
