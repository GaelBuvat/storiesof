# Generated by Django 3.0.5 on 2020-04-14 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storiesof', '0002_projects'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Projects',
            new_name='Project',
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Project'},
        ),
    ]
