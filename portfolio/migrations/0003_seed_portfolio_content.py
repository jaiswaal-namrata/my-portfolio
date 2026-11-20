from django.db import migrations


def seed_portfolio_content(apps, schema_editor):
    Profile = apps.get_model('portfolio', 'Profile')
    Skill = apps.get_model('portfolio', 'Skill')
    Project = apps.get_model('portfolio', 'Project')

    Profile.objects.get_or_create(
        pk=1,
        defaults={
            'full_name': 'Namrta Jaiswal',
            'job_title': 'Full-stack Developer',
            'summary': 'I build thoughtful, accessible web experiences with Python, Django, and modern front-end tools.',
        },
    )

    starter_skills = [
        ('HTML & CSS', 'Front-end', 82, 1),
        ('JavaScript & jQuery', 'Front-end', 72, 2),
        ('Python', 'Back-end', 76, 3),
        ('Django', 'Back-end', 72, 4),
        ('SQLite', 'Database', 68, 5),
    ]
    for name, category, proficiency, display_order in starter_skills:
        Skill.objects.get_or_create(
            name=name,
            defaults={
                'category': category,
                'proficiency': proficiency,
                'display_order': display_order,
            },
        )

    Project.objects.get_or_create(
        title='Namrta Jaiswal — Portfolio',
        defaults={
            'description': 'A responsive Django portfolio with database-backed contact messages and an editable content dashboard.',
            'technologies': 'Django, Python, HTML, CSS, JavaScript, SQLite',
            'theme': 'moss',
            'display_order': 1,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_profile_project_skill'),
    ]

    operations = [
        migrations.RunPython(seed_portfolio_content, migrations.RunPython.noop),
    ]
