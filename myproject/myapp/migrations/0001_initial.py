# Generated by Django 4.2.6 on 2023-10-24 08:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batches',
            fields=[
                ('batch_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course_heads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_head_number', models.BigIntegerField()),
                ('course_head_name', models.CharField(max_length=255)),
                ('contact', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('course_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=255)),
                ('course_head_id', models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.course_heads')),
            ],
        ),
        migrations.CreateModel(
            name='Faculties',
            fields=[
                ('faculty_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('faculty_name', models.CharField(max_length=255)),
                ('course_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.courses')),
            ],
        ),
        migrations.CreateModel(
            name='Lecturers',
            fields=[
                ('lecturer_number', models.BigIntegerField(primary_key=True, serialize=False)),
                ('lecturer_name', models.CharField(max_length=200)),
                ('lecturer_contact', models.BigIntegerField()),
                ('batch_id', models.ManyToManyField(to='myapp.batches')),
                ('course_id', models.ManyToManyField(to='myapp.courses')),
                ('faculty_id', models.ManyToManyField(to='myapp.faculties')),
            ],
        ),
        migrations.CreateModel(
            name='Program_heads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_head_number', models.BigIntegerField()),
                ('program_head_name', models.CharField(max_length=255)),
                ('contact', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('program_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('program_name', models.CharField(max_length=255)),
                ('program_type', models.CharField(choices=[('certificate', 'Certificate'), ('diploma', 'Diploma'), ('undergraduate', 'Undergraduate'), ('postgraduate', 'Postgraduate')], max_length=20)),
                ('batch_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.batches')),
                ('course_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.courses')),
                ('lecturer_id', models.ManyToManyField(default=None, to='myapp.lecturers')),
                ('program_head', models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.program_heads')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_code', models.CharField(editable=False, max_length=3, unique=True)),
                ('year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Year must be at least 1.'), django.core.validators.MaxValueValidator(6, message='Year must be at most 6.')])),
                ('semester', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Semester must be at least 1.'), django.core.validators.MaxValueValidator(3, message='Semester must be at most 3.')])),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('unit_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('unit_name', models.CharField(max_length=200)),
                ('batch_id', models.ManyToManyField(default=None, to='myapp.batches')),
                ('lecturer_id', models.ManyToManyField(default=None, to='myapp.lecturers')),
                ('program_id', models.ManyToManyField(default=None, to='myapp.programs')),
                ('time_code_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.time')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('student_number', models.BigIntegerField(primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=255)),
                ('batch_id', models.ManyToManyField(to='myapp.batches')),
                ('course_id', models.ManyToManyField(to='myapp.courses')),
                ('faculty_id', models.ManyToManyField(to='myapp.faculties')),
                ('program_id', models.ManyToManyField(to='myapp.programs')),
                ('time_code_id', models.ManyToManyField(to='myapp.time')),
            ],
        ),
        migrations.CreateModel(
            name='StudentClassification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_marks', models.DecimalField(decimal_places=1, max_digits=5)),
                ('classification', models.CharField(max_length=100)),
                ('batch_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.batches')),
                ('course_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.courses')),
                ('faculty_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.faculties')),
                ('program_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.programs')),
                ('student_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.students')),
            ],
        ),
        migrations.AddField(
            model_name='programs',
            name='student_id',
            field=models.ManyToManyField(default=None, to='myapp.students'),
        ),
        migrations.AddField(
            model_name='programs',
            name='units_id',
            field=models.ManyToManyField(default=None, to='myapp.units'),
        ),
        migrations.AddField(
            model_name='program_heads',
            name='program_id',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.programs'),
        ),
        migrations.AddField(
            model_name='lecturers',
            name='program_id',
            field=models.ManyToManyField(to='myapp.programs'),
        ),
        migrations.AddField(
            model_name='lecturers',
            name='time_code_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.time'),
        ),
        migrations.AddField(
            model_name='lecturers',
            name='units_id',
            field=models.ManyToManyField(to='myapp.units'),
        ),
        migrations.CreateModel(
            name='Faculty_heads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_head_number', models.BigIntegerField()),
                ('faculty_head_name', models.CharField(max_length=255)),
                ('contact', models.BigIntegerField()),
                ('faculty_id', models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.faculties')),
            ],
        ),
        migrations.AddField(
            model_name='faculties',
            name='faculty_head_id',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.faculty_heads'),
        ),
        migrations.AddField(
            model_name='faculties',
            name='lecturer_id',
            field=models.ManyToManyField(default=None, to='myapp.lecturers'),
        ),
        migrations.AddField(
            model_name='faculties',
            name='student_id',
            field=models.ManyToManyField(default=None, to='myapp.students'),
        ),
        migrations.CreateModel(
            name='Exams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.IntegerField()),
                ('grade', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1)),
                ('remarks', models.CharField(max_length=100)),
                ('batch_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.batches')),
                ('course_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.courses')),
                ('faculty_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.faculties')),
                ('invigilator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.lecturers')),
                ('program_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.programs')),
                ('student_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.students')),
                ('time_code_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.time')),
                ('unit_code_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.units')),
            ],
            options={
                'verbose_name_plural': 'Exams',
            },
        ),
        migrations.AddField(
            model_name='courses',
            name='faculty_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.faculties'),
        ),
        migrations.AddField(
            model_name='courses',
            name='lecturer_id',
            field=models.ManyToManyField(default=None, to='myapp.lecturers'),
        ),
        migrations.AddField(
            model_name='courses',
            name='program_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.programs'),
        ),
        migrations.AddField(
            model_name='courses',
            name='students_id',
            field=models.ManyToManyField(default=None, to='myapp.students'),
        ),
        migrations.AddField(
            model_name='course_heads',
            name='course_id',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.courses'),
        ),
        migrations.AddField(
            model_name='batches',
            name='lecturer_id',
            field=models.ManyToManyField(default=None, to='myapp.lecturers'),
        ),
        migrations.AddField(
            model_name='batches',
            name='program_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='myapp.programs'),
        ),
        migrations.AddField(
            model_name='batches',
            name='student_id',
            field=models.ManyToManyField(default=None, to='myapp.students'),
        ),
        migrations.AddField(
            model_name='batches',
            name='time_code_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='myapp.time'),
        ),
        migrations.AddField(
            model_name='batches',
            name='unit_id',
            field=models.ManyToManyField(default=None, to='myapp.units'),
        ),
    ]
