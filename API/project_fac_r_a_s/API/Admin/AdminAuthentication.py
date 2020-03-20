from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ..models import Admin 
from GlobalsValues.globalValues import *


class AdminAuthentication:

    def __init__(self):
        
        self.admin_user = None

        self.response_data = {}

    def handlingAdminLoginTask(self, request):

        request_data = request.data
        adminExistResp = self.checkAdminExist(request_data)

        if adminExistResp==False or adminExistResp==True:
            
            if adminExistResp:
                
                login(request, self.admin_user)
                self.response_data["msg"] = AUTHENTICATED_USER
                self.response_data["data"] = []
                self.response_data["status"] = "success"
                request.session['user_type'] = ADMIN
                return self.response_data

            else:
                self.response_data["msg"] = INVALID_CREDENTIALS
                self.response_data["data"] = []
                self.response_data["status"] = "error"
                print(self.response_data)
                return self.response_data
        else:
            print("################# invalid user type")
            return self.response_data

    def checkAdminExist(self, request_data):
        
        if 'user_type' in request_data and request_data['user_type']==ADMIN:

            admin_user = authenticate(username=request_data['email'], password=request_data['password'])
            self.admin_user = admin_user

            if admin_user:
                return True
            else:
                return False
        else:

            self.response_data["msg"] = INVALID_USER_TYPE
            self.response_data["data"] = []
            self.response_data["status"] = "invalid"
            return self.response_data