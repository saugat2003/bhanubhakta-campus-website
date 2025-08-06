from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    News, Notice, Gallery, Alumni, 
    SplashImage, StudentTestimonial, FacultyMember,
    Course, Facility, College, AdmissionApplication,
    Syllabus, Resource, Calendar, Contact
)
from .forms import AdmissionApplicationForm, AcademicQualificationFormSet, AdmissionDocumentFormSet, ContactForm

def home(request):
    # Handle contact form submission if it's a POST request
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        
        if contact_form.is_valid():
            # Get form data
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            phone = contact_form.cleaned_data.get('phone', 'Not provided')
            subject = contact_form.cleaned_data['subject']
            message = contact_form.cleaned_data['message']
            
            # Save to database
            contact_message = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            
            # Prepare email content
            email_subject = f"New Contact Form Submission: {subject}"
            email_message = f"""
New contact form submission from Bhanubhakta Campus website:

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}

---
This message was sent from the Bhanubhakta Campus website contact form.
Submitted at: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}
"""
            
            try:
                # Send email to campus
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                
                messages.success(
                    request, 
                    'Thank you for your message! We have received your inquiry and will get back to you soon.'
                )
                
            except Exception as e:
                # If email fails, still save to database but show different message
                messages.warning(
                    request,
                    'Your message has been saved, but there was an issue sending the email notification. We will still review your message.'
                )
                print(f"Email sending failed: {e}")  # For debugging
            
            return redirect('base:home')
        else:
            messages.error(request, 'Please correct the errors in the contact form.')
    else:
        contact_form = ContactForm()
    
    # Get latest news and notices for homepage
    latest_news = News.objects.filter(is_published=True).order_by('-published_date')[:3]
    latest_notices = Notice.objects.filter(is_published=True).order_by('-published_date')[:3]
    splash_images = SplashImage.objects.filter(is_published=True).order_by('order')
    testimonials = StudentTestimonial.objects.filter(is_published=True).order_by('-created_at')[:3]
    
    # Get gallery images for homepage gallery section
    gallery_images = Gallery.objects.filter(image__isnull=False).order_by('-uploaded_at')[:9]
    
    # Get faculty members for about section
    faculty_members = FacultyMember.objects.all()[:4]  # Featured faculty
    
    # Get courses for programs section
    courses = Course.objects.all()[:6]  # Show up to 6 courses
    
    # Get alumni for alumni section
    alumni = Alumni.objects.all().order_by('-batch_year')[:6]  # Show recent alumni
    
    # Get statistics (you can make these dynamic later)
    total_students = 2500  # Can be calculated from AdmissionForm or Student model later
    total_teachers = faculty_members.count()
    years_of_excellence = 30
    
    context = {
        'latest_news': latest_news,
        'latest_notices': latest_notices,
        'splash_images': splash_images,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
        'faculty_members': faculty_members,
        'courses': courses,
        'alumni': alumni,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'years_of_excellence': years_of_excellence,
        'contact_form': contact_form,  # Add contact form to context
    }
    return render(request, 'home.html', context)

def about(request):
    faculty_members = FacultyMember.objects.all()
    facilities = Facility.objects.all()
    
    context = {
        'faculty_members': faculty_members,
        'facilities': facilities,
    }
    return render(request, 'about.html', context)

def gallery(request):
    # Get all galleries that have images
    galleries = Gallery.objects.filter(image__isnull=False).order_by('-uploaded_at')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(galleries, 12)  # 12 images per page
    page_number = request.GET.get('page')
    galleries_page = paginator.get_page(page_number)
    
    context = {
        'galleries': galleries_page,
        'total_images': galleries.count(),
    }
    return render(request, 'gallery.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', 'Not provided')
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Save to database
            contact_message = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            
            # Prepare email content
            email_subject = f"New Contact Form Submission: {subject}"
            email_message = f"""
New contact form submission from Bhanubhakta Campus website:

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}

---
This message was sent from the Bhanubhakta Campus website contact form.
Submitted at: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}
"""
            
            try:
                # Send email to campus
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                
                messages.success(
                    request, 
                    'Thank you for your message! We have received your inquiry and will get back to you soon.'
                )
                
            except Exception as e:
                # If email fails, still save to database but show different message
                messages.warning(
                    request,
                    'Your message has been saved, but there was an issue sending the email notification. We will still review your message.'
                )
                print(f"Email sending failed: {e}")  # For debugging
            
            return redirect('base:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)

def faculty_members(request):
    """Display all faculty members with their details"""
    faculty_list = FacultyMember.objects.all().order_by('designation', 'full_name')
    
    # Pagination - 12 faculty members per page
    paginator = Paginator(faculty_list, 12)
    page_number = request.GET.get('page')
    faculty = paginator.get_page(page_number)
    
    context = {
        'faculty': faculty,
        'total_faculty': faculty_list.count(),
    }
    return render(request, 'faculty_member.html', context)

def admission(request):
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST, request.FILES)
        academic_formset = AcademicQualificationFormSet(request.POST, prefix='academic')
        document_formset = AdmissionDocumentFormSet(request.POST, request.FILES, prefix='document')
        
        if form.is_valid() and academic_formset.is_valid() and document_formset.is_valid():
            # Save the main admission application
            admission_application = form.save()
            
            # Save academic qualifications
            for academic_form in academic_formset:
                if academic_form.cleaned_data and not academic_form.cleaned_data.get('DELETE', False):
                    academic_qualification = academic_form.save(commit=False)
                    academic_qualification.application = admission_application
                    academic_qualification.save()
            
            # Save documents
            for document_form in document_formset:
                if document_form.cleaned_data and not document_form.cleaned_data.get('DELETE', False):
                    document = document_form.save(commit=False)
                    document.application = admission_application
                    document.save()
            
            messages.success(
                request, 
                f'Thank you! Your admission application for {admission_application.full_name} has been submitted successfully. '
                'Our admission team will contact you within 2-3 business days.'
            )
            return redirect('base:admission')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = AdmissionApplicationForm()
        academic_formset = AcademicQualificationFormSet(prefix='academic', queryset=None)
        document_formset = AdmissionDocumentFormSet(prefix='document', queryset=None)
    
    # Get all courses for display (if needed)
    courses = Course.objects.all()
    
    # Get facilities for display
    facilities = Facility.objects.all()
    
    # Get some stats for the admission page
    total_courses = courses.count()
    total_facilities = facilities.count()
    
    context = {
        'form': form,
        'academic_formset': academic_formset,
        'document_formset': document_formset,
        'courses': courses,
        'facilities': facilities,
        'total_courses': total_courses,
        'total_facilities': total_facilities,
    }
    return render(request, 'admission.html', context)

def notice(request):
    # Get all published notices with pagination
    notice_list = Notice.objects.filter(is_published=True).order_by('-published_date')
    
    # Pagination - 10 notices per page
    paginator = Paginator(notice_list, 10)
    page_number = request.GET.get('page')
    notices = paginator.get_page(page_number)
    
    context = {
        'notices': notices,
        'total_notices': notice_list.count(),
    }
    return render(request, 'notice.html', context)

def news(request):
    # Get all published news with pagination
    news_list = News.objects.filter(is_published=True).order_by('-published_date')
    
    # Pagination - 6 news articles per page
    paginator = Paginator(news_list, 6)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    # Get latest notices for sidebar
    latest_notices = Notice.objects.filter(is_published=True)[:5]
    
    context = {
        'news': news,
        'latest_notices': latest_notices,
        'total_news': news_list.count(),
    }
    return render(request, 'news.html', context)

def news_detail(request, pk):
    # Get specific news item
    news_item = get_object_or_404(News, pk=pk, is_published=True)
    
    # Get related/recent news (excluding current one)
    recent_news = News.objects.filter(is_published=True).exclude(pk=pk).order_by('-published_date')[:4]
    
    # Get latest notices for sidebar
    latest_notices = Notice.objects.filter(is_published=True)[:5]
    
    context = {
        'news': news_item,
        'recent_news': recent_news,
        'latest_notices': latest_notices,
    }
    return render(request, 'news_detail.html', context)

def notice_detail(request, pk):
    # Get specific notice
    notice_item = get_object_or_404(Notice, pk=pk, is_published=True)
    
    # Get recent notices (excluding current one)
    recent_notices = Notice.objects.filter(is_published=True).exclude(pk=pk).order_by('-published_date')[:5]
    
    # Get latest news for sidebar
    latest_news = News.objects.filter(is_published=True)[:5]
    
    context = {
        'notice': notice_item,
        'recent_notices': recent_notices,
        'latest_news': latest_news,
    }
    return render(request, 'notice_detail.html', context)

# Additional view for blog functionality (if needed)
def blog(request):
    # Using News model as blog posts
    blog_list = News.objects.filter(is_published=True).order_by('-published_date')
    
    # Pagination
    paginator = Paginator(blog_list, 5)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    
    context = {
        'blogs': blogs,
    }
    return render(request, 'blog.html', context)

def blog_detail(request, pk):
    # Using News model as blog posts
    blog_post = get_object_or_404(News, pk=pk, is_published=True)
    recent_posts = News.objects.filter(is_published=True).exclude(pk=pk).order_by('-published_date')[:3]
    
    context = {
        'blog': blog_post,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog_detail.html', context)

# Additional utility views and redirects

def event_detail_view(request, id=None):
    """Event detail view - currently redirects to news"""
    if id:
        # If specific event ID, try to find corresponding news item
        try:
            news_item = get_object_or_404(News, id=id, is_published=True)
            return redirect('base:news_detail', id=news_item.id)
        except:
            # If news item not found, redirect to news list
            return redirect('base:news')
    else:
        # If no ID provided, redirect to news list
        return redirect('base:news')

def admission_submit_view(request):
    """Handle admission form submission (alternative endpoint)"""
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)
        if form.is_valid():
            admission_application = form.save()
            messages.success(
                request, 
                f'Thank you! Your admission application for {admission_application.student_name} has been submitted successfully. '
                'Our admission team will contact you within 2-3 business days.'
            )
            return redirect('base:admission')
        else:
            messages.error(request, 'Please correct the errors in the form and try again.')
            return redirect('base:admission')
    else:
        return redirect('base:admission')

def admission_requirements(request):
    """View for admission requirements page"""
    courses = Course.objects.all()
    context = {
        'courses': courses,
        'page_title': 'Admission Requirements',
    }
    return render(request, 'admission_requirements.html', context)

def admission_process(request):
    """View for admission process page"""
    context = {
        'page_title': 'Admission Process',
    }
    return render(request, 'admission_process.html', context)

def fee_structure(request):
    """View for fee structure page"""
    courses = Course.objects.all()
    context = {
        'courses': courses,
        'page_title': 'Fee Structure',
    }
    return render(request, 'fee_structure.html', context)

def search_view(request):
    """Simple search functionality"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return redirect('base:home')
    
    # Search in news and notices
    news_results = News.objects.filter(
        title__icontains=query, 
        is_published=True
    )[:5]
    
    notice_results = Notice.objects.filter(
        title__icontains=query
    )[:5]
    
    context = {
        'query': query,
        'news_results': news_results,
        'notice_results': notice_results,
        'total_results': news_results.count() + notice_results.count()
    }
    
    # For now, redirect to news page with search context
    return render(request, 'news.html', context)

def api_news_view(request):
    """API endpoint for news (for AJAX requests)"""
    news_list = News.objects.filter(is_published=True).order_by('-created_at')[:10]
    
    news_data = []
    for news in news_list:
        news_data.append({
            'id': news.id,
            'title': news.title,
            'summary': news.summary,
            'created_at': news.created_at.strftime('%Y-%m-%d'),
            'image_url': news.featured_image.url if news.featured_image else None
        })
    
    return JsonResponse({'news': news_data})

@require_http_methods(["GET"])
def health_check_view(request):
    """Health check endpoint"""
    return JsonResponse({'status': 'healthy', 'timestamp': timezone.now().isoformat()})

def syllabus(request):
    """View for syllabus page"""
    # Get all syllabuses organized by course level
    bachelor_syllabuses = Syllabus.objects.filter(course__level='B').select_related('course').order_by('course__name')
    master_syllabuses = Syllabus.objects.filter(course__level='M').select_related('course').order_by('course__name')
    
    context = {
        'bachelor_syllabuses': bachelor_syllabuses,
        'master_syllabuses': master_syllabuses,
    }
    return render(request, 'syllabus.html', context)

def resources(request):
    """View for resources page with calendar section"""
    # Get all resources
    resources = Resource.objects.all().order_by('-uploaded_at')
    
    # Get latest academic calendar
    latest_calendar = Calendar.objects.order_by('-uploaded_at').first()
    
    # Get all calendars for archive
    all_calendars = Calendar.objects.all().order_by('-uploaded_at')
    
    context = {
        'resources': resources,
        'latest_calendar': latest_calendar,
        'all_calendars': all_calendars,
    }
    return render(request, 'resources.html', context)
