from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from GlobalsValues.globalValues import *
from django.core import serializers
import json
from .FetchPresentStudents import FetchPresentStudents
from API.models import *
from API.TokenDecorder import TokenDecorder

class FetchPresentStudentListView(APIView):

    def post(self, request):

        if request.user.is_authenticated:
            token_data = TokenDecorder(request.session.get('token', False), request).decodeSessionToken(checking_type="user_type_checking")
            if token_data and token_data['user_type']=="HOD":  

                getStudentListResp = FetchPresentStudents(request).getStudentList()

                if getStudentListResp["status"] == "success":
                    print("session response", request.session.get('token'))
                    return Response(
                        data=json.dumps(getStudentListResp),
                    status=status.HTTP_200_OK
                )

                elif getStudentListResp["status"] == "invalid":
                    return Response(
                        data=json.dumps(getStudentListResp),
                    status=status.HTTP_400_BAD_REQUEST
                )

                elif getStudentListResp["status"] == "error":
                    return Response(
                        data=json.dumps(getStudentListResp),
                    status=status.HTTP_400_BAD_REQUEST
                ) 
                
                else:
                    return Response(
                        data=json.dumps(getStudentListResp),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    ) 
            return Response(
                    data=json.dumps({
                        "msg":"not acceptable",
                        "data":[],
                        "status":"error"
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
                    status=status.HTTP_401_UNAUTHORIZED
                )