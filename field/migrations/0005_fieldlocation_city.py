# Generated by Django 5.2.3 on 2025-06-20 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field', '0004_field_size_field_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldlocation',
            name='city',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
