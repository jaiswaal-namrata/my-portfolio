from django.db import migrations


def add_provided_education(apps, schema_editor):
    Profile = apps.get_model('portfolio', 'Profile')
    Profile.objects.filter(education='').update(
        education='B.Tech in Computer Science and Engineering',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_alter_profile_job_title'),
    ]

    operations = [
        migrations.RunPython(add_provided_education, migrations.RunPython.noop),
    ]
