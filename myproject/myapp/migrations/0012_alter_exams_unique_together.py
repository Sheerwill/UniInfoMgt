# Generated by Django 4.2.6 on 2023-11-08 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_studentclassification_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='exams',
            unique_together={('unit_id', 'student_id')},
        ),
    ]