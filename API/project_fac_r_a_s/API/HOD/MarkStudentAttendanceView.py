from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from GlobalsValues.globalValues import *
from django.core import serializers
import json
from .MarkStudentAttendance import MarkStudentAttendance
from API.models import *
from API.TokenDecorder import TokenDecorder

class MarkStudentAttendanceView(APIView):

    def post(self, request):
        
        if request.user.is_authenticated:
            token_data = TokenDecorder(request.session.get('token', False), request).decodeSessionToken(checking_type="user_type_checking")

            if token_data['user_type']=="HOD":
                
                markStudentAttendanceResponse = MarkStudentAttendance(request).handlingAttendaceMarking()

                if markStudentAttendanceResponse["status"] == "success":
                    return Response(
                        data=json.dumps(markStudentAttendanceResponse),
                        status=status.HTTP_201_CREATED
                    )

                elif markStudentAttendanceResponse["status"] == "session_expired":
                    return Response(
                        data=json.dumps(markStudentAttendanceResponse),
                        status=status.HTTP_408_REQUEST_TIMEOUT
                    )
                elif markStudentAttendanceResponse["status"] == "not_found":
                    return Response(
                        data=json.dumps(markStudentAttendanceResponse),
                        status=status.HTTP_404_NOT_FOUND
                    )

                elif markStudentAttendanceResponse["status"] == "empty":
                    return Response(
                        data=json.dumps(markStudentAttendanceResponse),
                        status=status.HTTP_404_NOT_FOUND
                    )
                elif markStudentAttendanceResponse["status"] == "error":
                    return Response(
                        data=json.dumps(markStudentAttendanceResponse),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                elif markStudentAttendanceResponse["status"] == "invalid":
                    return Response(
                        data=json.dumps(markStudentAttendanceResponse),
                    status=status.HTTP_400_BAD_REQUEST
                )
                else:
                    return Response(
                        data=json.dumps(markStudentAttendanceResponse),
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