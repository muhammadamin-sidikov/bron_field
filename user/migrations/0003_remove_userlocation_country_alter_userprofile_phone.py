# Generated by Django 5.2.3 on 2025-06-18 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userlocation_district'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlocation',
            name='country',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
