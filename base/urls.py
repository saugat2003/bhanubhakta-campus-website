from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    # Home and basic pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admission/', views.admission, name='admission'),
    path('admission/submit/', views.admission_submit_view, name='admission_submit'),
    path('admission/requirements/', views.admission_requirements, name='admission_requirements'),
    path('admission/process/', views.admission_process, name='admission_process'),
    path('admission/fees/', views.fee_structure, name='fee_structure'),
    path('gallery/', views.gallery, name='gallery'),
    path('faculty/', views.faculty_members, name='faculty_members'),
    
    # News URLs
    path('news/', views.news, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    
    # Notice URLs
    path('notice/', views.notice, name='notice'),
    path('notice/<int:pk>/', views.notice_detail, name='notice_detail'),
    
    # Blog URLs (using News model)
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    
    # Event URLs (redirect to news)
    path('events/', views.event_detail_view, name='events'),
    path('events/<int:id>/', views.event_detail_view, name='event_detail'),
    
    # Academic Pages
    path('syllabus/', views.syllabus, name='syllabus'),
    path('resources/', views.resources, name='resources'),
    
    # Utility URLs
    path('search/', views.search_view, name='search'),
    path('api/news/', views.api_news_view, name='api_news'),
    path('health/', views.health_check_view, name='health_check'),
]
