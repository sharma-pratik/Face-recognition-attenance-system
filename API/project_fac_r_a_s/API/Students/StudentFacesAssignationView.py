
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from GlobalsValues.globalValues import *
from django.core import serializers
import json
from .AssignFaces import AssignFaces
from API.TokenDecorder import TokenDecorder


class StudentFacesAssignationView(APIView):

    def post(self, request):

        if request.user.is_authenticated:

            token_data = TokenDecorder(request.session.get('token', False), request).decodeSessionToken(checking_type="user_type_checking")

            if token_data['user_type']=="STUDENT":
                AssignationResp =  AssignFaces().handlingUploadFiles(request)    
                if AssignationResp['status']=="success":
                    return Response(
                        data=json.dumps(AssignationResp),
                        status=status.HTTP_202_ACCEPTED
                    )
                
                elif AssignationResp['status']=="invalid":
                    return Response(
                        data=json.dumps(AssignationResp),
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                elif AssignationResp['status']=="error":
                    return Response(
                        data=json.dumps(AssignationResp),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                elif AssignationResp['status']=="server_error":
                    return Response(
                        data=json.dumps(AssignationResp),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                elif AssignationResp['status']=="training_error":
                    return Response(
                        data=json.dumps(AssignationResp),
                        status=status.HTTP_501_NOT_IMPLEMENTED
                    )
                else:
                    return Response(
                        data=json.dumps(AssignationResp),
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