# Generated by Django 3.0.5 on 2020-04-14 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storiesof', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_url', models.CharField(blank=True, max_length=100)),
                ('linkedin_admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storiesof.ProfilLinkedinAdmin')),
            ],
            options={
                'verbose_name': 'Projects',
            },
        ),
    ]
