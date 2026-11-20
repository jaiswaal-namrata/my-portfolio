from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'contact message'
        verbose_name_plural = 'contact messages'

    def __str__(self):
        return f'{self.name} — {self.subject}'


class Profile(models.Model):
    full_name = models.CharField(max_length=120, default='Namrata Jaiswal')
    job_title = models.CharField(max_length=160, default='Python Full-Stack Developer')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=80, blank=True)
    proficiency = models.PositiveSmallIntegerField(
        default=75,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    THEME_CHOICES = [
        ('moss', 'Moss'),
        ('sand', 'Sand'),
        ('lavender', 'Lavender'),
        ('rose', 'Rose'),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    technologies = models.CharField(max_length=240, blank=True)
    key_features = models.TextField(blank=True, help_text='Enter one feature per line.')
    screenshot_url = models.URLField(
        blank=True,
        help_text='Optional URL for a real project screenshot.',
    )
    screenshot_path = models.CharField(
        max_length=255,
        blank=True,
        help_text='Optional path relative to portfolio static files.',
    )
    live_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='moss')
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title
