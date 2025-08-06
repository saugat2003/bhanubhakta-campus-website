from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    College, Course, Syllabus, FacultyMember, HeadOfCampus, 
    News, Notice, AdmissionApplication, AcademicQualification, AdmissionDocument, 
    Facility, Calendar, Resource, Gallery, Alumni, SplashImage, StudentTestimonial, Contact
)

# Customize admin site header and title
admin.site.site_header = "School Administration Panel"
admin.site.site_title = "School Admin"
admin.site.index_title = "Welcome to School Administration"


# Course Admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'course_code', 'has_syllabus')
    list_filter = ('level',)
    search_fields = ('name', 'course_code')
    ordering = ('level', 'name')
    
    def has_syllabus(self, obj):
        try:
            return bool(obj.syllabus)
        except:
            return False
    has_syllabus.boolean = True
    has_syllabus.short_description = 'Syllabus Available'

# Syllabus Admin
@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('course', 'file_link')
    search_fields = ('course__name',)
    
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
        return "No file"
    file_link.short_description = 'Syllabus File'

# Faculty Member Admin
@admin.register(FacultyMember)
class FacultyMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'designation', 'contact_email', 'phone_number', 'image_preview')
    list_filter = ('designation',)
    search_fields = ('full_name', 'designation', 'contact_email')
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'full_name', 'designation', 'image')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'phone_number')
        }),
        ('Biography', {
            'fields': ('bio',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Photo'


# News Admin
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published', 'image_preview')
    list_filter = ('is_published', 'published_date', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    list_editable = ('is_published',)
    
    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'content', 'image')
        }),
        ('Publishing', {
            'fields': ('author', 'is_published', 'published_date')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image'

# Notice Admin
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published', 'has_file')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    list_editable = ('is_published',)
    
    def has_file(self, obj):
        return bool(obj.file)
    has_file.boolean = True
    has_file.short_description = 'File Attached'

# Admission Application Admin with comprehensive view
@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'contact_number', 'nationality', 'result_status', 'submitted_at', 'is_processed', 'documents_count')
    list_filter = ('gender', 'nationality', 'result_status', 'is_processed', 'submitted_at')
    search_fields = ('full_name', 'email', 'contact_number', 'guardian_name')
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at', 'profile_photo_preview', 'application_summary', 'documents_summary')
    list_editable = ('is_processed',)
    # Custom actions
    actions = ['mark_as_processed', 'mark_as_unprocessed']

    fieldsets = (
        ('Admission Application Details', {
            'fields': (
                'application_summary',
                'profile_photo_preview', 'profile_photo',
                'full_name', 'date_of_birth_ad', 'date_of_birth_bs', 'nationality', 'gender',
                'permanent_address', 'temporary_address', 'contact_number', 'email',
                'other_qualification', 'result_status',
                'guardian_name', 'guardian_contact',
                'documents_summary',
                'is_processed', 'submitted_at'
            ),
            'classes': ('wide',),
        }),
    )

    def profile_photo_preview(self, obj):
        if obj.profile_photo:
            return format_html(
                '<div style="text-align: center;">'
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />'
                '<br><small style="color: #666;">Profile Photo</small>'
                '</div>',
                obj.profile_photo.url
            )
        return format_html('<div style="text-align: center; color: #999;">No profile photo uploaded</div>')
    profile_photo_preview.short_description = 'Profile Photo'

    def application_summary(self, obj):
        return format_html(
            '<div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #007bff;">'
            '<h3 style="margin-top: 0; color: #007bff;">Application Summary</h3>'
            '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">'
            '<div>'
            '<strong>Student Name:</strong> {}<br>'
            '<strong>Email:</strong> {}<br>'
            '<strong>Contact:</strong> {}<br>'
            '<strong>Nationality:</strong> {}<br>'
            '</div>'
            '<div>'
            '<strong>Guardian:</strong> {}<br>'
            '<strong>Guardian Contact:</strong> {}<br>'
            '<strong>Submitted:</strong> {}<br>'
            '<strong>Status:</strong> <span style="color: {};">{}</span><br>'
            '</div>'
            '</div>'
            '</div>',
            obj.full_name or 'Not provided',
            obj.email or 'Not provided',
            obj.contact_number or 'Not provided',
            obj.get_nationality_display(),
            obj.guardian_name or 'Not provided',
            obj.guardian_contact or 'Not provided',
            obj.submitted_at.strftime('%B %d, %Y at %I:%M %p'),
            '#28a745' if obj.is_processed else '#dc3545',
            '✅ Processed' if obj.is_processed else 'Pending'
        )
    application_summary.short_description = 'Application Overview'

    def documents_summary(self, obj):
        documents = obj.documents.all()
        if not documents.exists():
            return format_html('<div style="color: #dc3545;">⚠️ No documents uploaded</div>')

        docs_html = '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">'
        docs_html += '<h4 style="margin-top: 0; color: #28a745;">📁 Uploaded Documents ({} files)</h4>'.format(documents.count())
        docs_html += '<div style="display: grid; gap: 10px;">'

        for doc in documents:
            docs_html += format_html(
                '<div style="background: white; padding: 10px; border-radius: 5px; border: 1px solid #dee2e6;">'
                '<strong>📄 {}:</strong> '
                '<a href="{}" target="_blank" style="color: #007bff; text-decoration: none;">'
                '<i class="fas fa-download"></i> Download File'
                '</a>'
                '<small style="color: #6c757d; margin-left: 10px;">Uploaded: {}</small>'
                '</div>',
                doc.document_name,
                doc.document_file.url if doc.document_file else '#',
                doc.uploaded_at.strftime('%B %d, %Y')
            )

        docs_html += '</div></div>'
        return format_html(docs_html)
    documents_summary.short_description = 'Documents Uploaded'

    def documents_count(self, obj):
        count = obj.documents.count()
        if count > 0:
            return format_html('<span style="color: #28a745;">📁 {} files</span>', count)
        return format_html('<span style="color: #dc3545;">no files</span>')
    documents_count.short_description = 'Documents'

    def mark_as_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        self.message_user(request, f'{updated} applications marked as processed.')
    mark_as_processed.short_description = "Mark selected applications as processed"

    def mark_as_unprocessed(self, request, queryset):
        updated = queryset.update(is_processed=False)
        self.message_user(request, f'{updated} applications marked as unprocessed.')
    mark_as_unprocessed.short_description = "Mark selected applications as unprocessed"

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('full_name', 'date_of_birth_ad', 'date_of_birth_bs', 'nationality', 'gender',
                                          'permanent_address', 'temporary_address', 'contact_number', 'email',
                                          'other_qualification', 'result_status', 'guardian_name', 'guardian_contact')
        return self.readonly_fields

    class Media:
        css = {
            'all': ('admin/css/custom_admission_admin.css',)
        }
        js = ('admin/js/custom_admission_admin.js',)

# Calendar Admin
@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'academic_year', 'uploaded_at', 'file_link')
    list_filter = ('academic_year', 'uploaded_at')
    search_fields = ('title', 'academic_year')
    ordering = ('-uploaded_at',)
    
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
        return "No file"
    file_link.short_description = 'Calendar File'

# Resource Admin
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'file_link')
    search_fields = ('title', 'description')
    ordering = ('-uploaded_at',)
    
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
        return "No file"
    file_link.short_description = 'Resource File'

# Gallery Admin
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'image_preview')
    search_fields = ('title',)
    ordering = ('-uploaded_at',)
    fields = ('title', 'image')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image Preview'

# Alumni Admin
@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'batch_year', 'present_post', 'photo_preview')
    list_filter = ('batch_year',)
    search_fields = ('full_name', 'present_post', 'batch_year')
    ordering = ('-batch_year',)
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.photo.url)
        return "No photo"
    photo_preview.short_description = 'Photo'

# Splash Image Admin
@admin.register(SplashImage)
class SplashImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_published', 'image_preview')
    list_filter = ('is_published',)
    search_fields = ('title',)
    ordering = ('order',)
    list_editable = ('order', 'is_published')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: 60px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

# Student Testimonial Admin
@admin.register(StudentTestimonial)
class StudentTestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'designation', 'is_published', 'created_at', 'photo_preview')
    list_filter = ('is_published', 'created_at')
    search_fields = ('student_name', 'designation', 'message')
    ordering = ('-created_at',)
    list_editable = ('is_published',)
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'designation', 'photo')
        }),
        ('Testimonial', {
            'fields': ('message',)
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.photo.url)
        return "No photo"
    photo_preview.short_description = 'Photo'

# Contact Admin
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'submitted_at', 'is_replied', 'reply_status')
    list_filter = ('is_replied', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at', 'message_preview')
    list_editable = ('is_replied',)
    
    # Custom actions
    actions = ['mark_as_replied', 'mark_as_not_replied']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone'),
            'classes': ('wide',),
        }),
        ('Message Details', {
            'fields': ('subject', 'message_preview', 'message'),
            'classes': ('wide',),
        }),
        ('Response Status', {
            'fields': ('is_replied', 'submitted_at'),
            'classes': ('wide',),
        }),
    )
    
    def message_preview(self, obj):
        if obj.message:
            preview = obj.message[:200] + "..." if len(obj.message) > 200 else obj.message
            return format_html(
                '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff;">'
                '<h4 style="margin-top: 0; color: #007bff;">📧 Message Preview</h4>'
                '<p style="margin-bottom: 0; line-height: 1.5;">{}</p>'
                '</div>',
                preview
            )
        return "No message"
    message_preview.short_description = 'Message Preview'
    
    def reply_status(self, obj):
        if obj.is_replied:
            return format_html('<span style="color: #28a745;">✅ Replied</span>')
        return format_html('<span style="color: #dc3545;">⏳ Pending</span>')
    reply_status.short_description = 'Status'
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(is_replied=True)
        self.message_user(request, f'{updated} messages marked as replied.')
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    def mark_as_not_replied(self, request, queryset):
        updated = queryset.update(is_replied=False)
        self.message_user(request, f'{updated} messages marked as not replied.')
    mark_as_not_replied.short_description = "Mark selected messages as not replied"