from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='faculty_logos/', blank=True, null=True)

    def __str__(self):
        return self.name



class Semester(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        unique_together = ('faculty', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.faculty.name})"

class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    chapters = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.semester.name})"

class Notice(models.Model):
    NOTICE_TYPES = [
        ('program', 'Upcoming Program'),
        ('result', 'Result'),
        ('exam', 'Exam Date'),
        ('holiday', 'Holiday'),
        ('schedule', 'Class Schedule'),
    ]
    title = models.CharField(max_length=200)
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPES)
    description = models.TextField(blank=True,null=True)
    date = models.DateField()
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.date}"



class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_chapters')
    title = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.title} ({self.subject.name})"

class Note(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.chapter.title})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_members/')
    def __str__(self):
        return self.name

class SiteStatistics(models.Model):
    students_enrolled = models.PositiveIntegerField(default=0)
    subjects = models.PositiveIntegerField(default=0)
    qnas = models.PositiveIntegerField(default=0)
    total_visitors = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Site Statistics"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} - {self.email}"

class Syllabus(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='syllabi')
    file = models.FileField(upload_to='syllabi/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Syllabus for {self.semester.name} uploaded on {self.uploaded_at.strftime('%Y-%m-%d')}"
