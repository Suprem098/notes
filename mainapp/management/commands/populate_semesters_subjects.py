# from django.core.management.base import BaseCommand
# from mainapp.models import Semester, Subject, Faculty

# class Command(BaseCommand):
#     help = 'Populate semesters and subjects with sample data'

#     def handle(self, *args, **kwargs):
#         # Get or create a default faculty
#         faculty, _ = Faculty.objects.get_or_create(name='Default Faculty', slug='default-faculty')

#         semesters = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth']

#         # Dictionary mapping semester names to list of subjects (code, title)
#         semester_subjects = {
#             'first': [
#                 ('CACS101', 'Computer Fundamentals and Applications'),
#                 ('CASO102', 'Society & Technology'),
#                 ('CAEN103', 'English I'),
#                 ('CAMT104', 'Mathematics I'),
#                 ('CACS105', 'Digital Logic'),
#             ],
#             'second': [
#                 ('CACS151', 'C Programming'),
#                 ('CAAC152', 'Financial Accounting'),
#                 ('CAEN153', 'English II'),
#                 ('CAMT154', 'Mathematics II'),
#                 ('CACS155', 'Microprocessor and Computer Architecture'),
#             ],
#             'third': [
#                 ('CACS201', 'Data Structure and Algorithm'),
#                 ('CAST202', 'Probability & Statistics'),
#                 ('CACS203', 'System Analysis and Design'),
#                 ('CACS204', 'OOP in Java'),
#                 ('CACS205', 'Web Technology'),
#             ],
#             'fourth': [
#                 ('CACS251', 'Operating System'),
#                 ('CACS252', 'Numerical Methods'),
#                 ('CACS253', 'Software Engineering'),
#                 ('CACS254', 'Scripting Languages'),
#                 ('CACS255', 'Database Management System'),
#                 ('CAPJ256', 'Project I'),
#             ],
#             'fifth': [
#                 ('CACS301', 'MIS and e-Business'),
#                 ('CACS302', 'DotNet Technology'),
#                 ('CACS303', 'Computer Networking'),
#                 ('CAMG304', 'Introduction to Management'),
#                 ('CACS305', 'Computer Graphics and Animation'),
#             ],
#             'sixth': [
#                 ('CACS351', 'Mobile Programming'),
#                 ('CACS352', 'Distributed System'),
#                 ('CACS353', 'Applied Economics'),
#                 ('CACS354', 'Advance Java Programming'),
#                 ('CACS355', 'Network Programming'),
#                 ('CAPJ356', 'Project II'),
#             ],
#             'seventh': [
#                 ('CACS401', 'Cyber Law & Professional Ethics'),
#                 ('CACS402', 'Cloud Computing'),
#                 ('CAIN403', 'Internships'),
#                 ('CACS404', 'Image Processing'),
#                 ('CACS405', 'Database Administration'),
#                 ('CACS406', 'Network Administration'),
#                 ('CACS407', 'Software Project Management'),
#                 ('CACS408', 'Advanced .Net Technology'),
#                 ('CACS409', 'E-Governance'),
#                 ('CACS410', 'Artificial Intelligence'),
#                 ('CACS411', 'Applied Psychology'),
#             ],
#             'eighth': [
#                 ('CAOR451', 'Operational Research'),
#                 ('CAPJ452', 'Project III'),
#                 ('CACS453', 'Database Programming'),
#                 ('CACS454', 'Graphical Information System'),
#                 ('CACS455', 'Data Analysis & Visualization'),
#                 ('CACS456', 'Machine Learning'),
#                 ('CACS457', 'Multimedia System'),
#                 ('CACS458', 'Knowledge Engineering'),
#                 ('CACS459', 'Information Security'),
#                 ('CACS460', 'Internet of Things'),
#             ],
#         }

#         for sem_name in semesters:
#             semester, created = Semester.objects.get_or_create(name=sem_name, faculty=faculty)
#             if created:
#                 semester.slug = sem_name
#                 semester.save()
#                 self.stdout.write(self.style.SUCCESS(f'Semester "{sem_name}" created for faculty "{faculty.name}".'))
#             else:
#                 self.stdout.write(f'Semester "{sem_name}" already exists for faculty "{faculty.name}".')

#             # Populate subjects for the semester
#             subjects = semester_subjects.get(sem_name, [])
#             for code, title in subjects:
#                 subject, sub_created = Subject.objects.get_or_create(
#                     semester=semester,
#                     code=code,
#                     defaults={'name': title}
#                 )
#                 if sub_created:
#                     self.stdout.write(self.style.SUCCESS(f'Subject "{title}" ({code}) created for semester "{sem_name}".'))
#                 else:
#                     self.stdout.write(f'Subject "{title}" ({code}) already exists for semester "{sem_name}".')
