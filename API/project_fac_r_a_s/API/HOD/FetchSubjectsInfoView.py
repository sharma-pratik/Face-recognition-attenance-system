from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from GlobalsValues.globalValues import *
from django.core import serializers
import json
from .FetchPresentStudents import FetchPresentStudents
from API.models import *
from API.TokenDecorder import TokenDecorder
from .FetchSubjectsInfo import FetchSubjectsInfo

class FetchSubjectsInfoView(APIView):

    def post(self, request):
        
        if request.user.is_authenticated:
            token_data = TokenDecorder(request.session.get('token', False), request).decodeSessionToken(checking_type="user_type_checking")

            if token_data['user_type']=="HOD":
                
                fetchedSubjectInfoResp = FetchSubjectsInfo(request).fetchSubjects()
                if fetchedSubjectInfoResp["status"] == "success":
                    return Response(
                        data=json.dumps(fetchedSubjectInfoResp),
                        status=status.HTTP_302_FOUND
                    )

                else:
                    return Response(
                        data=json.dumps(fetchedSubjectInfoResp),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    ) 
                
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
