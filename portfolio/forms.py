from django import forms

from .models import ContactMessage, Profile, Project, Skill


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com', 'autocomplete': 'email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'What is this about?'}),
            'message': forms.Textarea(attrs={'placeholder': 'Tell me a little about your project...', 'rows': 5}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'job_title', 'email', 'phone', 'location', 'summary',
            'education', 'experience', 'linkedin_url', 'github_url',
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
            'education': forms.Textarea(attrs={'rows': 4, 'placeholder': 'One entry per line'}),
            'experience': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Role, organization, dates, and achievements'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'proficiency', 'display_order']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'technologies', 'key_features', 'screenshot_url',
            'screenshot_path', 'live_url', 'source_url', 'theme', 'display_order',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'technologies': forms.TextInput(attrs={'placeholder': 'Django, HTML, CSS'}),
            'key_features': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'One key feature per line',
            }),
            'screenshot_url': forms.URLInput(attrs={
                'placeholder': 'https://example.com/project-screenshot.png',
            }),
            'screenshot_path': forms.TextInput(attrs={
                'placeholder': 'portfolio/images/project-screenshot.png',
            }),
        }
