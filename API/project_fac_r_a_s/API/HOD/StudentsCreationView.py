from rest_framework.views import APIView
from .StudentsCreation import StudentsCreation
from API.TokenDecorder import TokenDecorder
from rest_framework import status
from rest_framework.response import Response
import json

class StudentsCreationView(APIView):

    def post(self, request):

        if request.user.is_authenticated:

            token_data = TokenDecorder(request.session.get('token', False), request).decodeSessionToken(checking_type="user_type_checking")

            if token_data['user_type']=="HOD":
                
                studentsCreationResp = StudentsCreation(request).handlingStudentsCreations()

                if studentsCreationResp["status"] == "success":
                    return Response(
                        data=json.dumps(studentsCreationResp),
                        status=status.HTTP_201_CREATED
                    )
                elif studentsCreationResp["status"] == "form_error":
                    return Response(
                        data=json.dumps(studentsCreationResp),
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )

                elif studentsCreationResp["status"] == "group_creation_error":
                    return Response(
                        data=json.dumps(studentsCreationResp),
                        status=status.HTTP_501_NOT_IMPLEMENTED
                    )

                elif studentsCreationResp["status"] == "network_error":
                    return Response(
                        data=json.dumps(studentsCreationResp),
                        status=status.HTTP_501_NOT_IMPLEMENTED
                    )
                elif studentsCreationResp["status"] == "error":
                    return Response(
                        data=json.dumps(studentsCreationResp),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                else:
                    return Response(
                        data=json.dumps(studentsCreationResp),
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
