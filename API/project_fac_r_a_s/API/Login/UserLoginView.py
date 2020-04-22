from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .UserAuthentication import UserAuthentication
from GlobalsValues.globalValues import *
from django.core import serializers
import json

class UserLoginView(APIView):

    def post(self, request):
        print(request.headers, request.user.is_authenticated, request.session.items(), request.session.session_key)

        if not request.user.is_authenticated:
            
            UserAuthenticateresponse = UserAuthentication().handlingUserLoginTask(request)

            if UserAuthenticateresponse["status"]=="invalid" and UserAuthenticateresponse["msg"] == INVALID_CREDENTIALS:

                return Response(
                    data=json.dumps(UserAuthenticateresponse),
                    status=status.HTTP_401_UNAUTHORIZED
                )

            elif UserAuthenticateresponse["status"]=="invalid" and UserAuthenticateresponse["msg"] == INVALID_USER_TYPE:
                print("UserAuthenticateresponse ",UserAuthenticateresponse )

                return Response(
                    data=json.dumps(UserAuthenticateresponse),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            elif UserAuthenticateresponse["status"]=="success":
                print("UserAuthenticateresponse ",request.session.items() )

                return Response(
                    data=json.dumps(UserAuthenticateresponse),
                    status=status.HTTP_202_ACCEPTED
                )

            else:
                print("UserAuthenticateresponse ",UserAuthenticateresponse )

                return Response(
                    data=json.dumps(UserAuthenticateresponse),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        else:
            print("already logged in", request.user.username)
            return Response(
                 data=json.dumps({
                    "msg":"already logged in",
                    "data":[],
                    "status":"success"
                }),
                status=status.HTTP_208_ALREADY_REPORTED
            )
            