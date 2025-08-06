from django import forms
from django.forms import modelformset_factory
from .models import AdmissionApplication, AcademicQualification, AdmissionDocument


class AdmissionApplicationForm(forms.ModelForm):
    # Override choice fields to add blank option at the beginning
    nationality = forms.ChoiceField(
        choices=[('', 'Select Nationality')] + list(AdmissionApplication.NATIONALITY_CHOICES),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
            'required': True
        })
    )
    
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender')] + list(AdmissionApplication.GENDER_CHOICES),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
            'required': True
        })
    )
    
    result_status = forms.ChoiceField(
        choices=[('', 'Select Result Status')] + list(AdmissionApplication.RESULT_STATUS_CHOICES),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
            'required': True
        })
    )

    class Meta:
        model = AdmissionApplication
        fields = [
            'profile_photo', 'full_name', 'date_of_birth_ad', 'date_of_birth_bs', 
            'nationality', 'gender', 'permanent_address', 'temporary_address', 
            'contact_number', 'email', 'other_qualification', 'result_status',
            'guardian_name', 'guardian_contact'
        ]
        
        widgets = {
            'profile_photo': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'accept': 'image/*'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Enter full name in BLOCK LETTERS',
                'style': 'text-transform: uppercase;',
                'required': True
            }),
            'date_of_birth_ad': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'type': 'date',
                'required': True
            }),
            'date_of_birth_bs': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'e.g., 2057/02/15',
                'required': True
            }),
            'permanent_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'rows': 3,
                'placeholder': 'Enter complete permanent address',
                'required': True
            }),
            'temporary_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'rows': 3,
                'placeholder': 'Enter complete temporary address',
                'required': True
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'e.g., +977-9841234567',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'other_qualification': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Specify organization if any'
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Enter guardian full name',
                'required': True
            }),
            'guardian_contact': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Guardian contact number',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mark required fields
        self.fields['full_name'].required = True
        self.fields['date_of_birth_ad'].required = True
        self.fields['date_of_birth_bs'].required = True
        self.fields['nationality'].required = True
        self.fields['gender'].required = True
        self.fields['permanent_address'].required = True
        self.fields['temporary_address'].required = True
        self.fields['contact_number'].required = True
        self.fields['email'].required = True
        self.fields['guardian_name'].required = True
        self.fields['guardian_contact'].required = True


class AcademicQualificationForm(forms.ModelForm):
    class Meta:
        model = AcademicQualification
        fields = [
            'institution_name', 'program', 'symbol_number', 'passed_year', 
            'percentage_cgpa', 'major_subjects'
        ]
        
        widgets = {
            'institution_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Institution Name'
            }),
            'program': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Program/Course'
            }),
            'symbol_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Symbol No.'
            }),
            'passed_year': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Passed Year'
            }),
            'percentage_cgpa': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Percentage/CGPA'
            }),
            'major_subjects': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Major Subjects'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AdmissionDocumentForm(forms.ModelForm):
    class Meta:
        model = AdmissionDocument
        fields = ['document_name', 'document_file']
        
        widgets = {
            'document_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
                'placeholder': 'Document Name'
            }),
            'document_file': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent'
            }),
        }


# Create formsets for multiple academic qualifications and documents
AcademicQualificationFormSet = modelformset_factory(
    AcademicQualification,
    form=AcademicQualificationForm,
    extra=2,  # Show 2 empty forms by default
    can_delete=True
)

AdmissionDocumentFormSet = modelformset_factory(
    AdmissionDocument,
    form=AdmissionDocumentForm,
    extra=3,  # Show 3 empty forms by default
    can_delete=True
)

# Contact Form
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
            'placeholder': 'Your Full Name',
            'required': True
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
            'placeholder': 'your.email@example.com',
            'required': True
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
            'placeholder': '+977 1234567890'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
            'placeholder': 'Subject of your message',
            'required': True
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-school-blue focus:border-transparent',
            'placeholder': 'Your message here...',
            'rows': 5,
            'required': True
        })
    )
