from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class Admin(models.Model):

    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, default=None, max_length=50)
    password = models.CharField(default=None, max_length=50)

class College(models.Model):
    college_name = models.CharField(max_length=100)
    college_code = models.IntegerField(unique=True)
    gtu_afflicated = models.BooleanField(default=False)
    domain = models.CharField(unique=True,max_length=50)

class CollegeManagement(models.Model):
    full_name = models.CharField(max_length=50)
    management_college_id = models.IntegerField()
    email = models.EmailField(unique=True, default=None, max_length=50)
    password = models.CharField(default=None, max_length=50)
    college = models.ForeignKey("College", on_delete=models.CASCADE)

class Faculty(models.Model):

    branch_choices = [
        ('Comp', 'Computer'),
        ('Mech', 'Mechanical'),
        ('IT', 'Information Technology'),
        ('Elect', 'Electrical'),
        ('EC', 'Electronic and communication'),
    ]

    class Meta:
        verbose_name = _("Faculty_model")

    def __str__(self):
        return "name: "+self.full_name+"gtu_id: "+self.gtu_id

    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, default=None, max_length=50)
    password = models.CharField(default=None, max_length=50)
    gtu_id = models.IntegerField()
    branch = models.CharField(max_length=30, choices=branch_choices)
    create_management_id = models.ForeignKey("CollegeManagement",null=True, on_delete=models.DO_NOTHING)
    create_hod_id = models.IntegerField(default=None, null=True)
    faculty_type_hod = models.BooleanField()
    college = models.ForeignKey("College", on_delete=models.CASCADE)

class Subject(models.Model):
    branch_choices = [
        ('Computer', 'Comp'),
        ('Mechanical', 'Mech'),
        ('Information Technology', 'IT'),
        ('Electrical', 'Elect'),
        ('Electronic and communication', 'EC'),
    ]

    subject_name = models.CharField(default=None, max_length=50)
    branch = models.CharField(max_length=30, choices=branch_choices)
    subject_code = models.IntegerField()
    faculty  = models.ForeignKey("Faculty",on_delete=models.DO_NOTHING)
    college = models.ForeignKey("College", on_delete=models.CASCADE)


class Periods(models.Model):
    weekday_choices = [
        ('Monday', 'mon'),
        ('Tuesday', 'tues'),
        ('Wednesday', 'wed'),
        ('Thursday', 'thur'),
        ('Friday', 'fri'),
        ('Saturday', 'sat'),
        ('Sunday', 'sun'),
    ]

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    period_number = models.IntegerField()
    semester = models.IntegerField()
    subject = models.ForeignKey("Subject",on_delete=models.CASCADE)
    week_day = models.CharField(max_length=10, choices=weekday_choices)
    subject_type_theory = models.BooleanField()
    room_number = models.IntegerField(null=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

class AttendanceTracking(models.Model):

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("")

    faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE)
    periods = models.ForeignKey("Periods", on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now=True, auto_now_add=False)
 
class Student(models.Model):
    
    branch_choices = [
        ('Computer', 'Comp'),
        ('Mechanical', 'Mech'),
        ('Information Technology', 'IT'),
        ('Electrical', 'Elect'),
        ('Electronic and communication', 'EC'),
    ]

    status = [
        ('detain', 'Detain'),
        ('active', 'Active'),
        ('passout', 'Passout'),
        ('leave', 'Leave')
    ]

    class Meta:
        verbose_name = _("Students")
        verbose_name_plural = _("Studentss")

    def __str__(self):
        return self.full_name

    full_name = models.CharField(max_length=50)
    email = models.EmailField( default=None, max_length=50)
    temperory_id = models.BigIntegerField()
    enrollment_id = models.BigIntegerField()
    semester_number = models.IntegerField()
    branch = models.CharField(max_length=30, choices=branch_choices)
    batch_year = models.CharField(max_length=50)
    sem_start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    sem_end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    student_status = models.CharField(max_length=20, choices=status)
    faculty = models.ForeignKey("Faculty", on_delete=models.DO_NOTHING)
    password = models.CharField(default=None, max_length=50)
    email_sent = models.BooleanField(default=False)
    college = models.ForeignKey("College", on_delete=models.CASCADE)

class AzureStudentFaces(models.Model):
    student = models.ForeignKey("Student",on_delete=models.CASCADE)
    azure_person_group_name = models.CharField(max_length=50)
    azure_person_id  = models.CharField(max_length=50)

class StudentFaceUrl(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    url = models.CharField(max_length=600)

class StudentAttendance(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.DO_NOTHING)
    total_subject_lectures = models.IntegerField()
    total_attend  = models.IntegerField()
    total_absent = models.IntegerField()
