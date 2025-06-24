from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import TeamMember, SiteStatistics, Feedback, Syllabus, BlogPost

admin.site.register(Feedback)
admin.site.register(TeamMember)
admin.site.register(SiteStatistics)
admin.site.register(Syllabus)
admin.site.register(BlogPost)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from .models import Faculty, Semester, Subject, Notice, Chapter, Note, ContactMessage

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    search_fields = ('name', 'faculty__name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester')
    list_filter = ('semester',)
    search_fields = ('name',)
    inlines = [ChapterInline]

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'notice_type', 'date', 'semester')
    list_filter = ('notice_type', 'semester')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    list_filter = ('subject',)
    search_fields = ('title',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter')
    list_filter = ('chapter',)
    search_fields = ('title',)
    autocomplete_fields = ['chapter']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')


