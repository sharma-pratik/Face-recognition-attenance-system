from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ..models import * 
from GlobalsValues.globalValues import *
import jwt
from project_fac_r_a_s.settings import JWTTokenSecretKey

class UserAuthentication:

    def __init__(self):
        
        self.active_user = None
        self.user_type_list = ['admin', 'hod', 'assistance_professor', 'management', 'student']

        self.response_data = {}
        self.session_data = {}
        self.user_data = {}

    def handlingUserLoginTask(self, request):

        self.checkUserExist(request)
            
        print(self.response_data)
        return self.response_data
    
    def checkUserExist(self, request):
        print(request.data)
        user_type = str(request.data['user_type']).lower()

        if 'user_type' in request.data  and user_type in self.user_type_list:

            if user_type == ADMIN:
                
                self.active_user = Admin.objects.filter(email=request.data['email']).values('full_name', 'email') 
                print(self.active_user)
                if self.active_user:
                    
                    if self.active_user[0]['password'] == request.data['password']:
                    
                        admin_user = authenticate(username=request.data['email'], password=request.data['password'])
                        login(request, admin_user)
                        self.createJWTToken(user_type, request)
                        self.response_data["msg"] = AUTHENTICATED_USER
                        self.response_data["data"] ={
                                "user_data":{
                                    "email":self.active_user[0]['email'],
                                    "full_name":self.active_user[0]['full_name']
                                },
                                "session_id": request.session.session_key
                            }
                        self.response_data["status"] = "success"

                    else:
                        self.response_data["msg"] = INVALID_CREDENTIALS
                        self.response_data["data"] = {"email":[], "password":"Password is invalid"}
                        self.response_data["status"] = "invalid"
                else:
                    print("élse")
                    self.response_data["msg"] = INVALID_CREDENTIALS
                    self.response_data["data"] = {"email":"Email does not exists", "password":[]}
                    self.response_data["status"] = "invalid"
                
            elif user_type == STUDENT:
                
                self.active_user = Student.objects.filter(email=request.data['email']).values('full_name', 'email', 'temperory_id', 'enrollment_id', 'semester_number', 'branch', 'batch_year', 'password') 
                
                if self.active_user:
                    
                    if self.active_user[0]['password'] == request.data['password']:
                        
                        student_user = authenticate(username=request.data['email'], password=request.data['password'])
                        login(request, student_user)
                        self.createJWTToken(user_type, request)
                        
                        self.response_data["msg"] = AUTHENTICATED_USER
                        self.response_data["data"] = {
                                "user_data":{
                                    "email":self.active_user[0]['email'],
                                    "full_name":self.active_user[0]['full_name'],
                                    "temperory_id":self.active_user[0]['temperory_id'],
                                    "enrollment_id": self.active_user[0]['enrollment_id'],
                                    "semester_number": self.active_user[0]['semester_number'],
                                    "branch": self.active_user[0]['branch'],
                                    "batch_year": self.active_user[0]['batch_year'],
                                },
                                "session_id": request.session.session_key
                            }
                        self.response_data["status"] = "success"

                    else:
                        self.response_data["msg"] = INVALID_CREDENTIALS
                        self.response_data["data"] = {"email":[], "password":"Password is invalid"}
                        self.response_data["status"] = "invalid"
                else:
                    self.response_data["msg"] = INVALID_CREDENTIALS
                    self.response_data["data"] = {"email":"Email does not exists", "password":[]}
                    self.response_data["status"] = "invalid"

            elif user_type == HOD:
        
                self.active_user = Faculty.objects.filter(email=request.data['email'], faculty_type_hod=True).values('full_name', 'email', 'faculty_id', 'branch', 'password','faculty_type_hod') 
                print(self.active_user)
                if self.active_user:
                    # email exists 
                    if self.active_user[0]['password'] == request.data['password']:

                        faculty_user = authenticate(username=request.data['email'], password=request.data['password'])
                        login(request, faculty_user)
                        self.createJWTToken(user_type, request)
                        
                        self.response_data["msg"] = AUTHENTICATED_USER
                        self.response_data["data"] = {
                            "user_data":{
                                "email":self.active_user[0]['email'],
                                "full_name":self.active_user[0]['full_name'],
                                "faculty_id":self.active_user[0]['faculty_id'],
                                "branch": self.active_user[0]['branch'],
                                "faculty_type": "HOD" if self.active_user[0]['faculty_type_hod'] else "Assitance Professor"
                            },
                                "session_id": request.session.session_key
                        }
                        self.response_data["status"] = "success"
                    else:
                        self.response_data["msg"] = INVALID_CREDENTIALS
                        self.response_data["data"] = {"email":[], "password":"Password is invalid"}
                        self.response_data["status"] = "invalid"

                else:
                    self.response_data["msg"] = INVALID_CREDENTIALS
                    self.response_data["data"] = {"email":"Email does not exists", "password":[]}
                    self.response_data["status"] = "invalid"
        else:
            print("invalid user type")
            self.response_data["msg"] = INVALID_USER_TYPE
            self.response_data["data"] = "Please select valid user type"
            self.response_data["status"] = "invalid"
            return self.response_data


    def createJWTToken(self, user_type, request):

        self.session_data["user_type"] = user_type
        session_token = jwt.encode(
            self.session_data,
            JWTTokenSecretKey,
             algorithm='HS256'
        )
        request.session["token"] = session_token.decode('utf-8')
        request.session.save()