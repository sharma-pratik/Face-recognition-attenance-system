from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ..models import * 
from GlobalsValues.globalValues import *
import jwt
from project_fac_r_a_s.settings import JWTTokenSecretKey

class UserAuthentication:

    def __init__(self):
        
        self.active_user = None
        self.user_type_list = ['Admin', 'HOD', 'Assistant Professor', 'Management', 'Student']

        self.response_data = {}
        self.session_data = {}

    def handlingUserLoginTask(self, request):

        userExistResp = self.checkUserExist(request)
        print("userExistResp ", userExistResp)
            
        if userExistResp==True:
            
            self.response_data["msg"] = AUTHENTICATED_USER
            self.response_data["data"] = [self.active_user[0]]
            self.response_data["status"] = "success"
            print("response_data ", self.response_data)
            return self.response_data

        elif userExistResp==False:
            self.response_data["msg"] = INVALID_CREDENTIALS
            self.response_data["data"] = [{"email":request.data['email'], "password":request.data['password'] }]
            self.response_data["status"] = "error"
            print("response_data ", self.response_data)
            return self.response_data
        else:   
            print("################# invalid user type")
            return self.response_data

    def checkUserExist(self, request):
        print(request.data)
        if 'user_type' in request.data  and request.data['user_type'] in self.user_type_list:
            user_type = str(request.data['user_type'])

            if user_type == ADMIN:
                    
                self.active_user = Admin.objects.filter(email=request.data['email'], password=request.data['password']).values('full_name', 'email') 
                if self.active_user:
                    admin_user = authenticate(username=request.data['email'], password=request.data['password'])
                    login(request, admin_user)
                    self.createJWTToken(user_type, request)

                    return True
                else:
                    return False
                
            elif user_type == STUDENT:
                
                self.active_user = Student.objects.filter(email=request.data['email'], password=request.data['password']).values('full_name', 'email', 'enrollment_id', 'semester_number', 'branch') 
                
                if self.active_user:

                    student_user = authenticate(username=request.data['email'], password=request.data['password'])
                    print()
                    login(request, student_user)
                    self.createJWTToken(user_type, request)


                    return True
                else:
                    return False

            elif user_type == HOD:
        
                self.active_user = Faculty.objects.filter(email=request.data['email'], password=request.data['password'], faculty_type_hod=True).values('full_name', 'email', 'faculty_id', 'branch') 
                if self.active_user:
                    faculty_user = authenticate(username=request.data['email'], password=request.data['password'])
                    print("faculty ", faculty_user)
                    login(request, faculty_user)
                    self.createJWTToken(user_type, request)
                    return True
                else:
                    return False
        else:
            self.response_data["msg"] = INVALID_USER_TYPE
            self.response_data["data"] = []
            self.response_data["status"] = "invalid"
            return self.response_data


    def createJWTToken(self, user_type, request):

        self.session_data["user_type"] = user_type
        session_token = jwt.encode(
            self.session_data,
            JWTTokenSecretKey,
             algorithm='HS256'
        )
        print(session_token)
        request.session["token"] = session_token.decode('utf-8')
        request.session.save()