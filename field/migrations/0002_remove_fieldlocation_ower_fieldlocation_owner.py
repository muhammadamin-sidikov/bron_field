# Generated by Django 5.2.3 on 2025-06-19 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldlocation',
            name='ower',
        ),
        migrations.AddField(
            model_name='fieldlocation',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='field_locations', to='field.field'),
            preserve_default=False,
        ),
    ]
