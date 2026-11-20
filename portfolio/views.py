from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm, ProfileForm, ProjectForm, SkillForm
from .models import ContactMessage, Profile, Project, Skill


def get_profile():
    profile, _ = Profile.objects.get_or_create(
        pk=1,
        defaults={
            'full_name': 'Namrata Jaiswal',
            'job_title': 'Python Full-Stack Developer',
            'summary': 'I build thoughtful, accessible web experiences with Python, Django, and modern front-end tools.',
        },
    )
    return profile


def staff_required(view):
    @wraps(view)
    @login_required(login_url='login')
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapped


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out. I'll get back to you soon.")
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'portfolio/home.html', {
        'form': form,
        'profile': get_profile(),
        'skills': Skill.objects.all(),
        'projects': Project.objects.all(),
    })


def resume(request):
    return render(request, 'portfolio/resume.html', {
        'profile': get_profile(),
        'skills': Skill.objects.all(),
        'projects': Project.objects.all(),
    })


@staff_required
def dashboard(request):
    profile = get_profile()
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile and resume details updated.')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'portfolio/dashboard.html', {
        'form': form,
        'skills': Skill.objects.all(),
        'projects': Project.objects.all(),
        'message_count': ContactMessage.objects.count(),
        'contact_messages': ContactMessage.objects.all()[:10],
    })


@staff_required
def skill_create(request):
    return skill_form(request)


@staff_required
def skill_edit(request, pk):
    return skill_form(request, get_object_or_404(Skill, pk=pk))


def skill_form(request, instance=None):
    form = SkillForm(request.POST if request.method == 'POST' else None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Skill saved.')
        return redirect('dashboard')
    return render(request, 'portfolio/manage_form.html', {
        'form': form,
        'item_type': 'skill',
        'page_title': 'Add skill' if instance is None else 'Edit skill',
    })


@staff_required
@require_POST
def skill_delete(request, pk):
    get_object_or_404(Skill, pk=pk).delete()
    messages.success(request, 'Skill deleted.')
    return redirect('dashboard')


@staff_required
def project_create(request):
    return project_form(request)


@staff_required
def project_edit(request, pk):
    return project_form(request, get_object_or_404(Project, pk=pk))


def project_form(request, instance=None):
    form = ProjectForm(request.POST if request.method == 'POST' else None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Project saved.')
        return redirect('dashboard')
    return render(request, 'portfolio/manage_form.html', {
        'form': form,
        'item_type': 'project',
        'page_title': 'Add project' if instance is None else 'Edit project',
    })


@staff_required
@require_POST
def project_delete(request, pk):
    get_object_or_404(Project, pk=pk).delete()
    messages.success(request, 'Project deleted.')
    return redirect('dashboard')
