from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .AdminAuthentication import AdminAuthentication
from GlobalsValues.globalValues import *
from django.core import serializers
import json
from .CollegeDeletion import CollegeDeletion

class DeleteCollegeView(APIView):

    def delete(self, request):

        if request.user.is_authenticated:
            
            user_type = request.session.get('user_type', False)

            if user_type and user_type=='Admin':
                collegeDeletionResp = CollegeDeletion().handlingCollegeDeletion(request)

                if collegeDeletionResp["status"]=="success":
                    return Response(
                        data=json.dumps(collegeDeletionResp),
                        status=status.HTTP_201_CREATED
                    )
                
                elif collegeDeletionResp["status"]=="error" and collegeDeletionResp["msg"]=="not found":
                    print(collegeDeletionResp)
                    return Response(
                        data=json.dumps(collegeDeletionResp),
                        status=status.HTTP_404_NOT_FOUND
                    )

                elif collegeDeletionResp["status"]=="error" and collegeDeletionResp["msg"]=="invalid":
                    return Response(
                        data=json.dumps(collegeDeletionResp),
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                else:
                    return Response(
                        data=json.dumps(collegeDeletionResp),
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

