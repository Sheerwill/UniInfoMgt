# Generated by Django 4.2.6 on 2023-11-08 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_exams_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programs',
            name='program_code',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
