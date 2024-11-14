# Generated by Django 4.2 on 2024-11-11 18:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('cin', models.CharField(max_length=8)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator])),
                ('password', models.CharField(max_length=20)),
                ('post', models.CharField(max_length=20)),
                ('VIP_statue', models.BooleanField()),
            ],
        ),
    ]