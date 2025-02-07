# Generated by Django 4.2 on 2024-11-07 21:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Art',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=50, unique=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('tags', models.CharField(blank=True, help_text='Tags séparés par des virgules', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='./arts/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'mp4', 'mp3'], message='Arts doit etre soit musique .mp3 ou .mp4 soit image :. jpg ou .png soit vidéo .mp4')])),
            ],
        ),
    ]
