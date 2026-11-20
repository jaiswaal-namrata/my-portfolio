from django.db import migrations


def set_portfolio_screenshot(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    Project.objects.filter(
        pk=1,
        title='Namrata Jaiswal — Portfolio',
        screenshot_path='',
    ).update(screenshot_path='portfolio/images/portfolio-project-preview.png')


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_project_screenshot_path'),
    ]

    operations = [
        migrations.RunPython(set_portfolio_screenshot, migrations.RunPython.noop),
    ]
