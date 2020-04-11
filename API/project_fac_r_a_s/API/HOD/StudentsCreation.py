from API.forms.StudentCreationForm import StudentCreationForm
from API.Services.GetAzurePersonGroup import GetAzurePersonGroup
from API.models import *
from django.contrib.auth.models import User
import datetime

class StudentsCreation:

    def __init__(self, request):
        super().__init__()  
        self.request = request
        self.faculty_obj = Faculty.objects.get(email=request.user.username)
        self.response_data = {}

    def handlingStudentsCreations(self):
        
        creationForm = StudentCreationForm(self.request.POST)

        if creationForm.is_valid():
            resp =  GetAzurePersonGroup(batch_year=self.request.POST['batch_year'],branch=self.request.POST['branch'], college_obj= Faculty.objects.get(email=self.request.user.username).college).handleAzurePersonGroup()
            
            print("response ", resp)
            if resp["status"] == "success":

                self.createStudent(resp["data"])
            else:
                self.response_data = resp    
        else:
            self.response_data["msg"] = "error"
            self.response_data["data"] = [ creationForm.errors.as_json()]
            self.response_data["status"] = "form_error"
        
        return self.response_data

    def createStudent(self, az_group):
        print("creating student")
        try:    
            stud_user_obj = User.objects.create_user( 
                username= self.request.POST["email"],
                password= 123456789
            )
        
            student_obj = Student.objects.create(
                full_name = self.request.POST["full_name"],
                email = self.request.POST["email"],
                enrollment_id = self.request.POST["enrollment_id"],
                semester_number = self.request.POST["semester_number"],
                branch = self.faculty_obj.branch,
                college = self.faculty_obj.college,
                batch_year = self.request.POST["batch_year"],
                student_status = self.request.POST["student_status"],
                sem_start_date = datetime.datetime(year=2019, month=12, day=1),
                sem_end_date = datetime.datetime(year=2020, month=7, day=1),
                faculty = self.faculty_obj,
                password = 123456789,
                azure_person_group = az_group,
            )

            subject_list = Subject.objects.filter(azure_person_group = az_group)

            print("subject list", subject_list)
            if subject_list:

                student_attendance_obj = []
                for single_sub in subject_list:
                    student_attendance_obj.append(
                        StudentAttendance(
                            student=student_obj,
                            subject = single_sub,
                            total_lectures = 40,
                            total_attend = 0,
                            total_absent = 0,
                            total_lectures_taken = 0
                        )
                    )

                StudentAttendance.objects.bulk_create(student_attendance_obj)
                print("subject assign to student")
            else:
                print("no subject to add")
            self.response_data["msg"] = "created successfully"
            self.response_data["data"] = []
            self.response_data["status"] = "success"

        except Exception as e:
            print("expcetion ", e)
            self.response_data["msg"] = "error occured"
            self.response_data["data"] = [e.args]
            self.response_data["status"] = "error"