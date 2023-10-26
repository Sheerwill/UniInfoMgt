from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

class Faculty_heads(models.Model):
    faculty_head_number = models.BigIntegerField()
    faculty_head_name = models.CharField(max_length=255)
    faculty_id = models.OneToOneField('Faculties', on_delete=models.PROTECT, default=None)
    contact = models.BigIntegerField()

#Faculties e.g Engineering
#No program field as courses have various programs. So programs are at the course level
#No batches for the same reason, No units
class Faculties(models.Model):
    faculty_code = models.CharField(max_length=255, primary_key=True)
    faculty_name = models.CharField(max_length=255) 
    faculty_head_id =  models.OneToOneField(Faculty_heads, on_delete=models.PROTECT, default=None) 
    student_id = models.ManyToManyField('Students', default=None)
    lecturer_id = models.ManyToManyField('Lecturers', default=None)
    course_id = models.ForeignKey('Courses', on_delete=models.PROTECT, default=None) 

class Course_heads(models.Model):
    course_head_number = models.BigIntegerField()
    course_head_name = models.CharField(max_length=255)
    course_id = models.OneToOneField('Courses', on_delete=models.PROTECT, default=None)
    contact = models.BigIntegerField()

#Courses e.g Electrical, Mechanical
#No batches as they're under programs, units also
class Courses(models.Model):
    course_code = models.CharField(max_length=255, primary_key=True)
    course_name = models.CharField(max_length=255)
    course_head_id = models.OneToOneField(Course_heads, on_delete=models.PROTECT, default=None)
    faculty_id = models.ForeignKey(Faculties, on_delete=models.PROTECT, default=None)
    students_id = models.ManyToManyField('Students', default=None)
    program_id = models.ForeignKey('Programs', on_delete=models.PROTECT, default=None)
    lecturer_id = models.ManyToManyField('Lecturers', default=None)

#Programs e.g EEEQ, EEEI ...
class Programs(models.Model):
    PROGRAM_TYPE_CHOICES = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
    ]
    program_code = models.CharField(max_length=255, primary_key=True)
    program_name = models.CharField(max_length=255) #e.g B.Eng, B.Sci, B.Tech
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPE_CHOICES) #e.g cert, dip, undergrad, pstgrad
    program_head = models.OneToOneField('Program_heads', on_delete=models.PROTECT, default=None)    
    batch_id = models.ForeignKey('Batches', on_delete=models.PROTECT, default=None)#One program has multiple batches
    units_id = models.ManyToManyField('Units', default=None) #One program has multiple units
    course_id = models.ForeignKey('Courses', on_delete=models.PROTECT, default=None)
    lecturer_id = models.ManyToManyField('Lecturers', default=None)#A program has multiple lecturers
    student_id = models.ManyToManyField('Students', default=None)  #A program has multiple students 

class Program_heads(models.Model):
    program_head_number = models.BigIntegerField()
    program_head_name = models.CharField(max_length=255)
    program_id = models.OneToOneField(Programs, on_delete=models.PROTECT, default=None)
    contact = models.BigIntegerField()
    

#Batches alphanumeric field e.g. 2013S or 2013PS ...
class Batches(models.Model):    
    batch_code = models.CharField(max_length=255, primary_key=True)
    program_id = models.ForeignKey(Programs, on_delete=models.PROTECT)    
    lecturer_id = models.ManyToManyField('Lecturers', default=None) #One batch is taught by multiple lecturers
    unit_id = models.ManyToManyField('Units', default=None)
    student_id = models.ManyToManyField('Students', default=None)
    time_code_id = models.ForeignKey('Time', on_delete=models.PROTECT, default=None)

class Time(models.Model):
    time_code = models.CharField(max_length=3, unique=True, editable=False)  # Max length is 3 (e.g., "1.1")
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Year must be at least 1."),
            MaxValueValidator(6, message="Year must be at most 6.")
        ]
    )
    semester = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Semester must be at least 1."),
            MaxValueValidator(3, message="Semester must be at most 3.")
        ]
    )    

    def save(self, *args, **kwargs):
        # Generate the time_code in the "year.semester" format
        self.time_code = f"{self.year}.{self.semester}"
        super(Time, self).save(*args, **kwargs)

    def __str__(self):
        return f"Year: {self.year}, Semester: {self.semester}, Time Code: {self.time_code}"

#students in a given batch
class Students(models.Model):
    student_number = models.BigIntegerField(primary_key=True)
    student_name = models.CharField(max_length=255)
    '''A student can be in multiple courses, they can therefore can be in multiple faculties, multiple programs 
    and have multiple batch ids'''
    faculty_id = models.ManyToManyField(Faculties)
    course_id = models.ManyToManyField(Courses)
    program_id = models.ManyToManyField(Programs)
    batch_id = models.ManyToManyField(Batches) 
    time_code_id = models.ManyToManyField(Time) 

    def __str__(self):
        return f"Student Number: {self.student_number}, Student Name: {self.student_name}"
    

#units in a given program
class Units(models.Model):
    unit_code = models.CharField(max_length=255, primary_key=True)
    unit_name = models.CharField(max_length=200)
    program_id = models.ManyToManyField(Programs, default=None) #One unit can be offered in multiple programs
    #Offered on what semester
    time_code_id = models.ForeignKey(Time, on_delete=models.PROTECT, default=None)
    #One unit can be taught by multiple lecturers
    lecturer_id = models.ManyToManyField('Lecturers', default=None)
    #Batches taking a given unit, units are taken by batches not students.
    batch_id = models.ManyToManyField(Batches, default=None)    

#lecturers in a given course
class Lecturers(models.Model):
    lecturer_number = models.BigIntegerField(primary_key=True)
    lecturer_name = models.CharField(max_length=200)
    lecturer_contact = models.BigIntegerField()         
    #A lecturer can be in multiple faculties e.g Business and in Engineering teaching business units 
    faculty_id = models.ManyToManyField(Faculties)    
    course_id = models.ManyToManyField(Courses) 
    program_id = models.ManyToManyField(Programs) #One Lecturer can teach in multiple programs
    batch_id = models.ManyToManyField(Batches) #One lecturer can teach multiple batches
    units_id = models.ManyToManyField(Units) #One lecturer can teach multiple units
    time_code_id = models.ForeignKey(Time, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.lecturer_name



class Exams(models.Model):
    unit_code_id = models.ForeignKey(Units, on_delete=models.CASCADE)
    invigilator = models.ForeignKey(Lecturers, on_delete=models.PROTECT, default=None)
    faculty_id = models.ForeignKey(Faculties, on_delete=models.PROTECT, default=None)
    course_id = models.ForeignKey(Courses, on_delete=models.PROTECT, default=None)
    program_id = models.ForeignKey(Programs, on_delete=models.CASCADE, default=None)
    batch_id = models.ForeignKey(Batches, on_delete=models.CASCADE, default=None)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, default=None)
    time_code_id = models.ForeignKey(Time, on_delete=models.PROTECT, default=None)
    percentage = models.IntegerField()
    grade = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')])
    remarks = models.CharField(max_length=100)

    def calculate_grade_and_remarks(self):
        if self.program_id.program_type == 'Postgraduate':
            if self.percentage >= 80:
                self.grade = 'A'
                self.remarks = 'Excellent'
            elif self.percentage >= 70:
                self.grade = 'B'
                self.remarks = 'Good'
            elif self.percentage >= 60:
                self.grade = 'C'
                self.remarks = 'Satisfactory'
            elif self.percentage >= 50:
                self.grade = 'D'
                self.remarks = 'Average/Pass'
            else:
                self.grade = 'E'
                self.remarks = 'Fail'
        else:
            if self.percentage >= 70:
                self.grade = 'A'
                self.remarks = 'Excellent'
            elif self.percentage >= 60:
                self.grade = 'B'
                self.remarks = 'Good'
            elif self.percentage >= 50:
                self.grade = 'C'
                self.remarks = 'Satisfactory'
            elif self.percentage >= 40:
                self.grade = 'D'
                self.remarks = 'Average/Pass'
            else:
                self.grade = 'E'
                self.remarks = 'Fail'

    def save(self, *args, **kwargs):
        self.calculate_grade_and_remarks()
        super(Exams, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.unit_code_id} - {self.student_id} - Grade: {self.grade} - Remarks: {self.remarks}'

    class Meta:
        verbose_name_plural = "Exams"

class StudentClassification(models.Model):
    faculty_id = models.ForeignKey(Faculties, on_delete=models.PROTECT, default=None)
    course_id = models.ForeignKey(Courses, on_delete=models.PROTECT, default=None)
    program_id = models.ForeignKey(Programs, on_delete=models.CASCADE, default=None)
    batch_id = models.ForeignKey(Batches, on_delete=models.CASCADE, default=None)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, default=None)
    average_marks = models.DecimalField(max_digits=5, decimal_places=1)
    classification = models.CharField(max_length=100)

    def calculate_classification(self):
        exams = Exams.objects.filter(student_id=self.student_id, program_id=self.program_id)

        if not exams:
            self.classification = ''  # No exams available
            return

        total_marks = sum(exam.percentage for exam in exams)
        average_marks = total_marks / len(exams)

        # Retrieve program_type from the associated program
        program_type = self.program_id.program_type

        # Calculate classification based on program type and average marks
        if program_type == 'Postgraduate':
            if average_marks >= 50:
                self.classification = 'Pass'
            else:
                self.classification = 'Fail'
        elif program_type == 'Undergraduate':
            if average_marks >= 70:
                self.classification = '1st Class Honors'
            elif 60 <= average_marks <= 69:
                self.classification = '2nd Class Honors Upper Division'
            elif 50 <= average_marks <= 59:
                self.classification = '2nd Class Honors Lower Division'
            elif 40 <= average_marks <= 49:
                self.classification = 'Pass'
        elif program_type in ['Certificate', 'Diploma']:
            if average_marks >= 70:
                self.classification = 'Distinction'
            elif 55 <= average_marks <= 69:
                self.classification = 'Credit'
            elif 40 <= average_marks <= 54:
                self.classification = 'Pass'

    def save(self, *args, **kwargs):
        self.calculate_classification()
        super(StudentClassification, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.student_id} - Classification: {self.classification}'