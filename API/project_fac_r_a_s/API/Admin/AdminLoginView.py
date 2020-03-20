from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .AdminAuthentication import AdminAuthentication
from GlobalsValues.globalValues import *
from django.core import serializers
import json


class AdminLoginView(APIView):

    def post(self, request):
        print(request.headers, request.user.is_authenticated, request.session.items())
        AdminAuthenticateresponse = AdminAuthentication().handlingAdminLoginTask(request)

        if not request.user.is_authenticated:
            if AdminAuthenticateresponse["status"]=="error" and AdminAuthenticateresponse["msg"] == INVALID_CREDENTIALS:
                return Response(
                    data=json.dumps(AdminAuthenticateresponse),
                    status=status.HTTP_401_UNAUTHORIZED
                )

            elif AdminAuthenticateresponse["status"]=="invalid" and AdminAuthenticateresponse["msg"] == INVALID_USER_TYPE:
                return Response(
                    data=json.dumps(AdminAuthenticateresponse),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            elif AdminAuthenticateresponse["status"]=="success":
                return Response(
                    data=json.dumps(AdminAuthenticateresponse),
                    status=status.HTTP_202_ACCEPTED
                )

            else:
                return Response(
                    data=json.dumps(AdminAuthenticateresponse),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        else:
            return Response(
                 data=json.dumps({
                    "msg":"already logged in",
                    "data":[],
                    "status":"success"
                }),
                status=status.HTTP_208_ALREADY_REPORTED
            )
            