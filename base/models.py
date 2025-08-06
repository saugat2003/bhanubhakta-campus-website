# models.py for your Django college website app
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# The core model for the college itself. This can be used for general site information.
class College(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    motto = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

# Model for the different academic courses offered
class Course(models.Model):
    # Using choices to define the course levels
    LEVEL_CHOICES = (
        ('B', 'Bachelor'),
        ('M', 'Master'),
    )
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, default='B')
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, help_text="Course image for display")
    
    def __str__(self):
        return f"{self.get_level_display()} - {self.name}"

# Model for a course's syllabus, linked via a one-to-one relationship
class Syllabus(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True)
    file = models.FileField(upload_to='syllabuses/', help_text="Upload the course syllabus as a PDF file.")
    
    def __str__(self):
        return f"Syllabus for {self.course.name}"

# Model for faculty and staff members, with an image field
class FacultyMember(models.Model):
    # One-to-one link to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='faculty_images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.full_name

# Model for campus heads, linking to a FacultyMember
class HeadOfCampus(models.Model):
    head = models.OneToOneField(FacultyMember, on_delete=models.CASCADE, primary_key=True)
    position = models.CharField(max_length=100, help_text="e.g., Campus Chief, Chairman")
    message = models.TextField()
    
    def __str__(self):
        return f"{self.position} - {self.head.full_name}"

# Model for news articles
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-published_date']
        verbose_name_plural = "News"
        
    def __str__(self):
        return self.title

# Model for notices and announcements
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    file = models.FileField(upload_to='notices/', blank=True, null=True, help_text="Optional PDF file for the notice.")
    
    class Meta:
        ordering = ['-published_date']
        
    def __str__(self):
        return self.title

# Model for a student's admission form submission
class AdmissionApplication(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    NATIONALITY_CHOICES = [
        ('nepali', 'Nepali'),
        ('other', 'Other'),
    ]
    
    RESULT_STATUS_CHOICES = [
        ('passed', 'Passed'),
        ('awaited', 'Awaited'),
    ]
    
    
    # Profile Photo
    profile_photo = models.ImageField(upload_to='admission_photos/', blank=True, null=True, verbose_name="Profile Photo")
    
    # Personal Information
    full_name = models.CharField(max_length=100, verbose_name="Full Name (Block Letters)", default="")
    date_of_birth_ad = models.DateField(verbose_name="Date of Birth (A.D.)", null=True, blank=True)
    date_of_birth_bs = models.CharField(max_length=20, verbose_name="Date of Birth (B.S.)", help_text="e.g., 2057/02/15", default="", blank=True)
    nationality = models.CharField(max_length=20, choices=NATIONALITY_CHOICES, default='nepali')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    permanent_address = models.TextField(verbose_name="Permanent Address", default="", blank=True)
    temporary_address = models.TextField(verbose_name="Temporary Address", default="", blank=True)
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number", default="", blank=True)
    email = models.EmailField(verbose_name="Email Address", default="", blank=True)
    
    # Academic Qualifications
    other_qualification = models.CharField(max_length=200, blank=True, null=True, verbose_name="Any Other Qualification (Specify Organization)")
    result_status = models.CharField(max_length=10, choices=RESULT_STATUS_CHOICES, default='passed')
    
    # Guardian Details
    guardian_name = models.CharField(max_length=100, verbose_name="Name of Guardian", default="", blank=True)
    guardian_contact = models.CharField(max_length=20, verbose_name="Guardian's Contact Number", default="", blank=True)
    
    # System fields
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Admission Application"
        verbose_name_plural = "Admission Applications"
    
    def __str__(self):
        return f"Admission Application - {self.full_name}"


# Model for Academic Qualifications (separate table for multiple entries)
class AcademicQualification(models.Model):
    
    application = models.ForeignKey(AdmissionApplication, on_delete=models.CASCADE, related_name='academic_qualifications')
    institution_name = models.CharField(max_length=200, verbose_name="Institution Name")
    program = models.CharField(max_length=100, verbose_name="Program/Course")
    symbol_number = models.CharField(max_length=50, verbose_name="Symbol Number")
    passed_year = models.CharField(max_length=10, verbose_name="Passed Year")
    percentage_cgpa = models.CharField(max_length=20, verbose_name="Percentage/CGPA")
    major_subjects = models.TextField(verbose_name="Major Subjects")
    
    class Meta:
        verbose_name = "Academic Qualification"
        verbose_name_plural = "Academic Qualifications"
    
    def __str__(self):
        return f"{self.institution_name} - {self.program}"


# Model for Document Uploads
class AdmissionDocument(models.Model):
    application = models.ForeignKey(AdmissionApplication, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=100, verbose_name="Document Name")
    document_file = models.FileField(upload_to='admission_documents/', verbose_name="Document File")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Admission Document"
        verbose_name_plural = "Admission Documents"
    
    def __str__(self):
        return f"{self.document_name} - {self.application.full_name}"

# Model for campus facilities
class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='facility_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Facilities"

    def __str__(self):
        return self.name

# Model for the academic calendar (PDF)
class Calendar(models.Model):
    title = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=10)
    file = models.FileField(upload_to='calendars/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.academic_year})"

# Model for resources, like downloadable academic papers or guides
class Resource(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resources/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# --- Models for Gallery Feature ---

# Model for an image gallery
class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery_images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, help_text="Title of the gallery")
    class Meta:
        verbose_name_plural = "Galleries"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

# --- Model for Alumni ---
class Alumni(models.Model):
    full_name = models.CharField(max_length=100)
    batch_year = models.CharField(max_length=10, help_text="e.g., 2018-2022")
    present_post = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='alumni_photos/', blank=True, null=True)
    message = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Alumni"
        ordering = ['-batch_year']

    def __str__(self):
        return f"{self.full_name} ({self.batch_year})"

# --- Model for Splash Images ---

class SplashImage(models.Model):
    """
    Model for homepage splash/carousel images.
    It's recommended to limit this to a maximum of 3 images via admin configuration.
    """
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='splash_images/')
    order = models.PositiveIntegerField(default=0, help_text="Order in which the image should appear.")
    is_published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Splash Images"
        ordering = ['order']

    def __str__(self):
        return self.title

# --- New Model for Student Testimonials ---

class StudentTestimonial(models.Model):
    student_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=150, help_text="e.g., 'BBS, 2022'")
    message = models.TextField()
    photo = models.ImageField(upload_to='testimonials_photos/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Student Testimonials"

    def __str__(self):
        return f"Testimonial from {self.student_name}"


# --- Contact Model for storing contact form submissions ---

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_replied = models.BooleanField(default=False, verbose_name="Replied")
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"