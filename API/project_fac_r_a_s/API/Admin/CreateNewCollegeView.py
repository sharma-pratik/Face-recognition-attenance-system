from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .AdminAuthentication import AdminAuthentication
from GlobalsValues.globalValues import *
from django.core import serializers
import json
from .CollegeCreation import CollegeCreation



class CreateNewCollegeView(APIView):

    def post(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            
            user_type = request.session.get('user_type', False)

            if user_type:
                collegeCreationResp = CollegeCreation().handleCollegeCreation(request)

                if collegeCreationResp["status"]=="success":
                    return Response(
                        data=json.dumps(collegeCreationResp),
                        status=status.HTTP_201_CREATED
                    )
                
                elif collegeCreationResp["status"]=="error" and collegeCreationResp["msg"]=="form error":
                    return Response(
                        data=json.dumps(collegeCreationResp),
                        status=status.HTTP_400_BAD_REQUEST
                    )

                elif collegeCreationResp["status"]=="error" and collegeCreationResp["msg"]==UNKNOWN_ERROR:
                    return Response(
                        data=json.dumps(collegeCreationResp),
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        data=json.dumps(collegeCreationResp),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return Response(
                    data=json.dumps({
                        "msg":UNAUTHEORIZED_USER,
                        "data":[],
                        "status":"invalid"
                    }),
                    status=status.HTTP_401_UNAUTHORIZED
                )

        else:
             return Response(
                    data=json.dumps({
                        "msg":"Please login to ",
                        "data":[],
                        "status":"error"
                    }),
                    status=status.HTTP_400_BAD_REQUEST
                )








# {
#     "user_type":"Admin",
#     "email":"pratik",
# 	"password":"pratik@123"
# }