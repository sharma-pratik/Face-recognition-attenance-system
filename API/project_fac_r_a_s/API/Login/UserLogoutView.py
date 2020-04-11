from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .UserAuthentication import UserAuthentication
from GlobalsValues.globalValues import *
from django.core import serializers
import json
from django.contrib.auth import logout

class UserLogoutView(APIView):

    def post(self, request):

        if request.user.is_authenticated:
            
            logout(request)

            return Response(
                 data=json.dumps({
                    "msg":"logged out successfully",
                    "data":[],
                    "status":"success"
                }),
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                 data=json.dumps({
                    "msg":"already logged out",
                    "data":[],
                    "status":"success"
                }),
                status=status.HTTP_208_ALREADY_REPORTED
            )
