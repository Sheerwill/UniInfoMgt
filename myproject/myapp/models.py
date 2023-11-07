from django.db import models, IntegrityError
from django.core.validators import MinValueValidator, MaxValueValidator

#Faculties e.g Engineering
#No program field as courses have various programs. So programs are at the course level
#No batches for the same reason, No units
class Faculties(models.Model):
    faculty_code = models.CharField(max_length=255)
    faculty_name = models.CharField(max_length=255)     

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return self.faculty_code

#Courses e.g Electrical, Mechanical
#No batches as they're under programs, units also
class Courses(models.Model):
    course_code = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)    
    faculty_id = models.ForeignKey(Faculties, on_delete=models.PROTECT, default=None)

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.course_code

#Programs e.g EEEQ, EEEI ...
class Programs(models.Model):
    PROGRAM_TYPE_CHOICES = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
    ]
    program_code = models.CharField(max_length=255)
    program_name = models.CharField(max_length=255) #e.g B.Eng, B.Sci, B.Tech
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPE_CHOICES) #e.g cert, dip, undergrad, pstgrad    
    course_id = models.ForeignKey(Courses, on_delete=models.PROTECT, default=None)

    class Meta:
        verbose_name_plural = "Programs"

    def __str__(self):
        return self.program_code

#Year and semester e.g 1.1, 1.2, 2.1, 2.2
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
    
    class Meta:
        verbose_name_plural = "Times"

    def __str__(self):
        return self.time_code
    
#Batches alphanumeric field e.g. 2013S or 2013PS ...
class Batches(models.Model):    
    batch_code = models.CharField(max_length=255)
    program_id = models.ForeignKey(Programs, on_delete=models.PROTECT)       
    time_id = models.ForeignKey(Time, on_delete=models.PROTECT, default=None)

    class Meta:
        verbose_name_plural = "Batches"

    def __str__(self):
        return self.batch_code

#students in a given batch
class Students(models.Model):    
    student_number = models.CharField(max_length=255, unique=True)
    student_name = models.CharField(max_length=255)     
    batch_id = models.ManyToManyField(Batches)      

    def __str__(self):        
        return self.student_number 
    
    class Meta:
        verbose_name_plural = "Students"   

#lecturers in a given course
#Upwards reference is made. Units a lecturer teaches are in Units
class Lecturers(models.Model):
    lecturer_number = models.BigIntegerField(unique=True)
    lecturer_name = models.CharField(max_length=200)
    lecturer_contact = models.BigIntegerField()       
    batch_id = models.ManyToManyField(Batches) #One lecturer can teach multiple batches    

    def __str__(self):
        return self.lecturer_number
    
    class Meta:
        verbose_name_plural = "Lecturers"   
  

#units in a given program
class Units(models.Model):
    unit_code = models.CharField(max_length=255, unique=True)
    unit_name = models.CharField(max_length=200)    
    #Offered on what semester
    time_id = models.ManyToManyField(Time)
    #One unit can be taught by multiple lecturers
    lecturer_id = models.ManyToManyField(Lecturers, default=None)
    #Batches taking a given unit, units are taken by batches not students.
    batch_id = models.ManyToManyField(Batches, default=None) 

    class Meta:
        verbose_name_plural = "Units" 

    def __str__(self):
        return self.unit_code  

#Assuming the invigilator is the unit lecturer
class Exams(models.Model):
    #exam_id = models.CharField(max_length=50, default=None) #Each exam has a unique id
    unit_id = models.ForeignKey(Units, on_delete=models.PROTECT, default=None)  
    #Exams are taken by individuals not batches  
    student_id = models.ForeignKey(Students, on_delete=models.PROTECT)    
    percentage = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        blank=True,
        default=0
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    grade = models.CharField(max_length=4, choices=[('', None), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], blank=True, default=None, editable=False)
    remarks = models.CharField(max_length=100, blank=True, editable=False)

    
    def save(self, *args, **kwargs):
        # Calculate grade and remarks
        if self.percentage is not None:
            student = self.student_id
            # Retrieve all batches associated with the student
            batches = student.batch_id.all()
            if batches.exists():
                # Assuming the program is the same for all batches (may need to refine this logic)
                program = batches[0].program_id      
                if program.program_type == 'Postgraduate':
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
        
        super(Exams, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.unit_id.unit_name} - {self.student_id} - {self.percentage} - Grade: {self.grade} - Remarks: {self.remarks}'

    class Meta:
        verbose_name_plural = "Exams"

#Students will register for graduation
#This reduces the amount of computations made just by one entry into the exams model
class StudentClassification(models.Model):
    faculty_id = models.ForeignKey(Faculties, on_delete=models.PROTECT, default=None)
    course_id = models.ForeignKey(Courses, on_delete=models.PROTECT, default=None)
    program_id = models.ForeignKey(Programs, on_delete=models.CASCADE, default=None)
    batch_id = models.ForeignKey(Batches, on_delete=models.CASCADE, default=None)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, default=None)
    average_marks = models.DecimalField(max_digits=5, decimal_places=1, blank=True, default=0.0)
    classification = models.CharField(max_length=100, blank=True, editable=False)

    def calculate_classification(self):
        program_id = self.program_id
        exams = Exams.objects.filter(student_id=self.student_id, student_id__batch_id__program_id=program_id)       

        if not exams:            
            self.classification = ''  # No exams available
            self.average_marks = 0.0  # Set a default value when no exams are available
            return                          

        total_marks = sum(exam.percentage for exam in exams)
        
        average_marks = total_marks / len(exams)

        self.average_marks = average_marks        

        # Retrieve program_type from the associated program
        program_type = program_id.program_type 
              

        # Calculate classification based on program type and average marks
        if program_type == 'postgraduate':
            if average_marks >= 50:
                self.classification = 'Pass'
            else:
                self.classification = 'Fail'
        elif program_type == 'undergraduate':
            if average_marks >= 70:                
                self.classification = '1st Class Honors'
            elif 60 <= average_marks <= 69:
                self.classification = '2nd Class Honors Upper Division'
            elif 50 <= average_marks <= 59:
                self.classification = '2nd Class Honors Lower Division'
            elif 40 <= average_marks <= 49:
                self.classification = 'Pass'
            else:
                self.classification = 'Fail'
        elif program_type in ['certificate', 'diploma']:
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
    
    class Meta:
        verbose_name_plural = "StudentClassifications"