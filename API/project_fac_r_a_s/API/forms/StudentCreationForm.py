from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import *
from django.utils.translation import gettext_lazy as _
import datetime
from API.models import *
from django.db.models import Q

class StudentCreationForm(forms.Form):
  
    branch_choices = [
        ('Comp', 'Computer'),
        ('Mech', 'Mechanical'),
        ('IT', 'Information Technology'),
        ('Elect', 'Electrical'),
        ('EC', 'Electronic and communication'),
    ]

    status = [
        ('detain', 'Detain'),
        ('active', 'Active'),
        ('passout', 'Passout'),
        ('leave', 'Leave')
    ]
    
    batch_year_list = []
    current_year = datetime.datetime.now().year
    num_of_year = current_year - 2010

    for i in range(num_of_year):
        batch_year_list.append(( str(current_year)+"-"+str(current_year+1),str(current_year)+"-"+str(current_year+1) ) )
        current_year = current_year-1

    def validate_fullname(value):
        print(value)
        try:
            validate_slug(value)
        except Exception as e:
            raise forms.ValidationError(_('invalid full name'))

    def validate_enrollment_id(value):
        
        if len(str(value)) is not 12:
            raise forms.ValidationError("Invalid enrollment number length")

    full_name = forms.CharField(max_length=50, label='Enter full name')
    email = forms.CharField( max_length=100, label='Enter email', validators=[ EmailValidator(message="Please enter a valid email") ])
    enrollment_id = forms.IntegerField(label='Enter enrollment number', validators=[validate_enrollment_id])
    semester_number = forms.IntegerField(label="Enter semeseter value")
    branch = forms.ChoiceField(label="Select branch",choices=branch_choices)
    batch_year = forms.ChoiceField(label="Select batch year", choices=batch_year_list)
    student_status = forms.ChoiceField(label="Select student status", choices=status)

    def clean(self):

        super().clean()
        enrollment_id = self.cleaned_data.get('enrollment_id', False)
        email = self.cleaned_data.get('email', False)


        if enrollment_id and email:
            stu_obj = Student.objects.filter(Q(enrollment_id=enrollment_id) | Q(email=email))
            if stu_obj:
                if email == stu_obj[0].email:
                    self.add_error('email', "email already exists")    
                elif enrollment_id == stu_obj[0].enrollment_id:
                    self.add_error('enrollment_id', "enrollment_id already exists")    
                




