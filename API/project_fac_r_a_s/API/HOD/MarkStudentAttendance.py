from API.TokenDecorder import TokenDecorder
from API.models import *
from django.db.models import F
import jwt
from project_fac_r_a_s.settings import JWTTokenSecretKey


class MarkStudentAttendance:

    def __init__(self, request):
        
        super().__init__()
        self.request = request
        self.subject_id = None
        self.response_data = {}

    def handlingAttendaceMarking(self):

        print(self.request.data.get('student_list'))
        
        if self.checkStudentListInput():
            
            self.updateStudentSubjectDetails()
            print(self.response_data)
            return self.response_data

        else:
            return self.response_data
    

    def checkStudentListInput(self):
        print(self.request.data.get("student_list", False), 'present_students' in self.request.data['student_list'], 'absent_students' in self.request.data['student_list'], 'subject_id' in self.request.data["student_list"])

        if self.request.data.get("student_list", False) and 'present_students' in self.request.data['student_list'] and 'absent_students' in self.request.data['student_list'] and 'subject_id' in self.request.data["student_list"]:

            if type( self.request.data['student_list']["present_students"] ) is type([]) and type( self.request.data['student_list']["absent_students"] is type([]) and type(self.request.data['subject_id']) is type("") ):
                print("true")
                return True

        print("invalid")
        self.response_data["msg"]= "invalid request type"
        self.response_data["data"] = []
        self.response_data["status"] = "invalid"

    def updateStudentSubjectDetails(self):
        try:
            present_Student_obj_list = Student.objects.filter(enrollment_id__in=self.request.data['student_list']['present_students'])
            absent_Student_obj_list = Student.objects.filter(enrollment_id__in=self.request.data['student_list']['absent_students'])
            
            print(present_Student_obj_list, absent_Student_obj_list)

            if self.isSubjectSessionExpired()==False:
                if present_Student_obj_list or absent_Student_obj_list:
                    try:
                        StudentAttendance.objects.filter(
                            student__in=present_Student_obj_list,
                            subject = Subject.objects.get(alpha_numeric_id = self.subject_id)
                        ).update(
                            total_attend = F('total_attend') + 1,
                            total_lectures_taken = F('total_lectures_taken') + 1
                        )

                        StudentAttendance.objects.filter(
                            student__in=absent_Student_obj_list,
                            subject = Subject.objects.get(alpha_numeric_id = self.subject_id)
                        ).update(
                            total_absent = F('total_absent') + 1,
                            total_lectures_taken = F('total_lectures_taken') + 1
                        )

                        self.response_data["msg"] = "added"
                        self.response_data["data"] = [] 
                        self.response_data["status"] = "success"
                        self.deleteSessionToken()
                    except Exception as e:
                        self.response_data["msg"] = "try again later"
                        self.response_data["data"] = [e.args] 
                        self.response_data["status"] = "error"
                else:
                    self.response_data["msg"] = "no data to add"
                    self.response_data["data"] = [] 
                    self.response_data["status"] = "empty"
        except Exception as e:
            self.response_data["msg"] = "try again later"
            self.response_data["data"] = [e.args] 
            self.response_data["status"] = "error"

    def isSubjectSessionExpired(self):
        token_data = TokenDecorder( self.request.session.get('token', False), self.request ).decodeSessionToken(checking_type="user_type_checking") 
        
        if "subject_token" in token_data:
            subject_token = TokenDecorder( token_data["subject_token"], self.request ).decodeSessionToken() 
            
            if subject_token and not subject_token=="expired":
                token_subject_id = subject_token["subject_alpha_id"]

                if self.request.data['student_list']['subject_id'] == token_subject_id:
                    print("subject is valid")
                    self.subject_id = self.request.data['student_list']['subject_id']
                    return False
                else:
                    print("subject not valid")
                    self.response_data["msg"] = "subject_id is not valid"
                    self.response_data["data"] = []
                    self.response_data["status"] = "error"
                    return "invalid"


            elif subject_token == "expired":
                print("in else expired")
                self.response_data["msg"] = "try again submitting photos"
                self.response_data["data"] = []
                self.response_data["status"] = "session_expired"
        else:
            self.response_data["msg"] = "Please fetch students details again by uploading photo"
            self.response_data["data"] = []
            self.response_data["status"] = "not_found"

    def deleteSessionToken(self):

        token_data_res = TokenDecorder(self.request.session.get('token'), self.request).decodeSessionToken()

        if not token_data_res == "expired" and token_data_res:
            del token_data_res["subject_token"]

            print("after deltin subject token ", token_data_res)
            session_token = jwt.encode(token_data_res, JWTTokenSecretKey, algorithm='HS256')
            
            self.request.session["token"] = session_token.decode('utf-8')
            self.request.session.save()
