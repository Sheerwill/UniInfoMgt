# Generated by Django 4.2.6 on 2023-10-27 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_exams_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exams',
            name='percentage',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
