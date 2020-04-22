from API.models import *
from django.db.models import *

class StudentAttendanceDetails:

    def __init__(self, request):
        super().__init__()
        self.request = request
        self.response_data = {}

    def fetchAttendanceDetails(self):

        try:
            student_obj = Student.objects.get(email =  self.request.user.username )

            totalAttendanceOverview = StudentAttendance.objects.filter(
                student =  student_obj
            ).aggregate(
                total = Sum('total_lectures'),
                attend_lectures = Sum('total_attend'),
                not_attend_lectures = Sum('total_absent')
            )

            lectures_details = list(
                    StudentAttendance.objects.filter(
                    student = student_obj
                ).values('total_lectures', 'total_attend', 'subject__subject_name')
            )

            for each in lectures_details:
                val = each.pop("subject__subject_name")
                each["subject_name"] = val

            final_data = {}
            final_data["total"] = totalAttendanceOverview
            final_data["subjects"] = lectures_details

            self.response_data["msg"] = ""
            self.response_data["data"] = final_data
            self.response_data["status"] = "success"
            return self.response_data
        except Exception as e:
            print(e)
            self.response_data["msg"] = "error"
            self.response_data["data"] = e.args
            self.response_data["status"] = "error"
