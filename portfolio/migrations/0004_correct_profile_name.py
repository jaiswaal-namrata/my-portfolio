from django.db import migrations, models


def correct_seeded_names(apps, schema_editor):
    Profile = apps.get_model('portfolio', 'Profile')
    Project = apps.get_model('portfolio', 'Project')

    Profile.objects.filter(full_name='Namrta Jaiswal').update(full_name='Namrata Jaiswal')
    Project.objects.filter(title='Namrta Jaiswal — Portfolio').update(
        title='Namrata Jaiswal — Portfolio',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_seed_portfolio_content'),
    ]

    operations = [
        migrations.RunPython(correct_seeded_names, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(default='Namrata Jaiswal', max_length=120),
        ),
    ]
