# Generated by Django 4.2.6 on 2023-11-07 06:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_studentclassification_average_marks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exams',
            name='percentage',
            field=models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
