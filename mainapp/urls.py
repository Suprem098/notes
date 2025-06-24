from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('about-us/', views.about_us, name='about_us'),
    path('feedback/', views.feedback, name='feedback'),
    path('syllabus-upload/', views.syllabus_list, name='syllabus_upload'),
    path('community/', views.community_list, name='community'),
    path('community/create/', views.community_create, name='community_create'),
    path('community/<int:post_id>/', views.community_detail, name='community_detail'),
    path('community/<int:post_id>/delete/', views.community_delete, name='community_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='mainapp/sign_in.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
