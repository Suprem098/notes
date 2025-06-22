import json
from django.shortcuts import render
from .models import TeamMember, SiteStatistics

def about_us(request):
    team_members = TeamMember.objects.all()
    stats = SiteStatistics.objects.first()
    context = {
        'team_members': team_members,
        'stats': stats,
    }
    return render(request, 'aboutus.html', context)
from .models import Semester, Subject, Notice, Chapter, Note, Faculty
import os
from django.conf import settings

def home(request):
    try:
        faculty = Faculty.objects.get(slug='default-faculty')
        semesters = faculty.semesters.all()
    except Faculty.DoesNotExist:
        semesters = []
    context = {
        'current_page': 'home',
        'semesters': semesters,
    }
    return render(request, 'mainapp/home.html', context)

def semester_detail(request, semester_slug):
    try:
        faculty = Faculty.objects.get(slug='default-faculty')
        semester = faculty.semesters.get(slug__iexact=semester_slug)
        semester_subjects = semester.subjects.all()
        print(f"DEBUG: Faculty: {faculty}, Semester: {semester}, Subjects count: {semester_subjects.count()}")
    except (Faculty.DoesNotExist, Semester.DoesNotExist):
        semester_subjects = []
        faculty = None
        semester = None
        print(f"DEBUG: Faculty or Semester not found for slug=default-faculty, semester_slug={semester_slug}")
    context = {
        'faculty': faculty,
        'semester_name': semester.name if semester else "Unknown Semester",
        'subjects': semester_subjects if semester else [],
        'current_page': 'semester',
    }
    return render(request, 'mainapp/semester_detail.html', context)

def notices(request):
    notices_qs = Notice.objects.all().order_by('-date')
    notices_data = {
        'upcoming_programs': list(notices_qs.filter(notice_type='program')),
        'results': list(notices_qs.filter(notice_type='result')),
        'exam_dates': list(notices_qs.filter(notice_type='exam')),
        'holidays': list(notices_qs.filter(notice_type='holiday')),
        'class_schedules': list(notices_qs.filter(notice_type='schedule')),
    }
    calendar_notices = {}
    for notice in notices_qs:
        date_str = notice.date.strftime('%Y-%m-%d')
        calendar_notices.setdefault(date_str, []).append({'title': notice.title, 'type': notice.notice_type})

    context = {
        'notices': notices_data,
        'notices_json': json.dumps(calendar_notices),
        'current_page': 'notices',
    }
    return render(request, 'mainapp/notices.html', context)

def sign_in(request):
    context = {'current_page': 'account'}
    return render(request, 'mainapp/sign_in.html', context)

def create_account(request):
    context = {'current_page': 'account'}
    return render(request, 'mainapp/create_account.html', context)

from django.shortcuts import redirect
from .models import ContactMessage

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            return render(request, 'mainapp/contact.html', {
                'current_page': 'contact',
                'success': True,
            })
        else:
            return render(request, 'mainapp/contact.html', {
                'current_page': 'contact',
                'error': 'Please fill in all fields.',
            })
    else:
        context = {'current_page': 'contact'}
        return render(request, 'mainapp/contact.html', context)

def chapter_list(request, semester_name):
    try:
        semester = Semester.objects.get(name__iexact=semester_name)
        subjects = semester.subjects.all()
        chapters = []
        for subject in subjects:
            chapters.extend(subject.subject_chapters.all())
    except Semester.DoesNotExist:
        chapters = []
    context = {
        'semester_name': semester_name.title(),
        'chapters': chapters,
        'current_page': 'semester',
    }
    return render(request, 'mainapp/chapter_list.html', context)

def chapter_list_by_subject(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
        chapters = subject.subject_chapters.all()
    except Subject.DoesNotExist:
        chapters = []
        subject = None
    context = {
        'semester_name': subject.semester.name.title() if subject else "Unknown Semester",
        'chapters': chapters,
        'current_page': 'semester',
    }
    return render(request, 'mainapp/chapter_list.html', context)

def semester_note_list(request, semester_name):
    try:
        semester = Semester.objects.get(name__iexact=semester_name)
        subjects = semester.subjects.all()
        chapters = []
        for subject in subjects:
            chapters.extend(subject.subject_chapters.all())
        chapters_with_notes = []
        for idx, chapter in enumerate(chapters, start=1):
            notes = chapter.notes.all()
            chapters_with_notes.append({
                'chapter': chapter,
                'notes': notes,
                'chapter_number': idx,
            })
    except Semester.DoesNotExist:
        chapters_with_notes = []
        semester_name = None
    context = {
        'semester_name': semester_name.title() if semester_name else "Unknown Semester",
        'chapters_with_notes': chapters_with_notes,
        'current_page': 'semester',
    }
    return render(request, 'mainapp/note_list.html', context)

def note_list(request, chapter_id):
    try:
        chapter = Chapter.objects.get(id=chapter_id)
        notes = chapter.notes.all()
    except Chapter.DoesNotExist:
        notes = []
    for note in notes:
        if note.file and not note.file.url.startswith('http'):
            scheme = 'https' if request.is_secure() else 'http'
            host = request.get_host()
            note.absolute_file_url = f"{scheme}://{host}{note.file.url}"
    context = {
        'chapter': chapter,
        'notes': notes,
        'current_page': 'semester',
    }
    return render(request, 'mainapp/note_list_single.html', context)

def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    file_exists = False
    if note.file:
        file_path = os.path.join(settings.MEDIA_ROOT, note.file.name)
        file_exists = os.path.exists(file_path)
    context = {
        'note': note,
        'file_exists': file_exists,
        'current_page': 'semester',
    }
    return render(request, 'mainapp/note_detail.html', context)

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

@csrf_exempt
def feedback(request):
    from .models import Feedback
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            # Save feedback to database
            Feedback.objects.create(
                name=name,
                email=email,
                message=message
            )
            return render(request, 'mainapp/feedback.html', {
                'success': True,
                'current_page': 'feedback',
            })
        else:
            return render(request, 'mainapp/feedback.html', {
                'error': 'Please fill in all fields.',
                'current_page': 'feedback',
            })
    else:
        return render(request, 'mainapp/feedback.html', {
            'current_page': 'feedback',
        })
