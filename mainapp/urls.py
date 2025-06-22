from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('semester/<slug:semester_slug>/', views.semester_detail, name='semester_detail'),
    path('semester/<slug:semester_slug>/chapters/', views.chapter_list, name='chapter_list'),
    path('subject/<int:subject_id>/chapters/', views.chapter_list_by_subject, name='chapter_list_by_subject'),
    path('semester/<slug:semester_slug>/notes/', views.semester_note_list, name='semester_note_list'),
    path('chapter/<int:chapter_id>/notes/', views.note_list, name='note_list'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('account/signin/', views.sign_in, name='sign_in'),
    path('account/create/', views.create_account, name='create_account'),
    path('notices/', views.notices, name='notices'),
    path('contact/', views.contact, name='contact'),
]
