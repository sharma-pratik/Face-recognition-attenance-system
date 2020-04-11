from rest_framework.views import APIView
from rest_framework import status
from API.TokenDecorder import TokenDecorder
from rest_framework.response import Response
from GlobalsValues.globalValues import *
from .StudentAttendanceDetails import StudentAttendanceDetails
import json

class StudentAttendanceDetailsView(APIView):

    def post(self,request):

        print(request)

        if request.user.is_authenticated:

            token_data = TokenDecorder(request.session.get('token', False), request).decodeSessionToken(checking_type="user_type_checking")

            if token_data['user_type']==STUDENT:
                
                attendanceDetailResp = StudentAttendanceDetails(request).fetchAttendanceDetails()
                if attendanceDetailResp["status"] == "success":
                    return Response(
                        data=json.dumps(attendanceDetailResp),
                        status=status.HTTP_302_FOUND
                    )
                else:
                    return Response(
                        data=json.dumps({
                            "msg":"error",
                            "data":[],
                            "status":"error"
                         }),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            else:
                return Response(
                    data=json.dumps({
                        "msg":"unauthorized",
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