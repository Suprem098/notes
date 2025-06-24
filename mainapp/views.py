import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import TeamMember, SiteStatistics, BlogPost
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404
from django.contrib import messages
from django.utils import timezone
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

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'mainapp/create_account.html', {'current_page': 'account'})

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'mainapp/create_account.html', {'current_page': 'account'})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'mainapp/create_account.html', {'current_page': 'account'})

        user = User.objects.create_user(username=username, password=password)
        user.save()

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'mainapp/create_account.html', {'current_page': 'account'})

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
from django.contrib import messages
from .forms import SyllabusForm
from .models import Syllabus

@csrf_exempt
def feedback(request):
    from .models import Feedback
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            
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



def syllabus_list(request):
    syllabi = Syllabus.objects.select_related('semester').all().order_by('uploaded_at')
    return render(request, 'mainapp/syllabus_list.html', {'syllabi': syllabi})

def community_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
        'current_page': 'community',
    }
    return render(request, 'mainapp/community.html', context)

@login_required
def community_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            BlogPost.objects.create(
                title=title,
                content=content,
                author=request.user,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            messages.success(request, 'Blog post created successfully.')
            return redirect('community')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'mainapp/community_create.html', {'current_page': 'community'})

def community_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    context = {
        'post': post,
        'current_page': 'community',
    }
    return render(request, 'mainapp/community_detail.html', context)
