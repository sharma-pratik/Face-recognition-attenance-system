import os
import uuid
from API.validators.ValidateUploadedFiles import ValidateUploadedFiles
from GlobalsValues.globalValues import *
from project_fac_r_a_s.settings import AWSSecretKey, AWSAccessKeyId, AzureKey, AzureEndpoint
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
import math
from API.models import *
import shutil
import json
import jwt
import datetime
from API.TokenDecorder import TokenDecorder
from project_fac_r_a_s.settings import JWTTokenSecretKey

class FetchPresentStudents:

    def __init__(self, request):

        super().__init__()
        self.request = request
        self.upload_folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'TempCreatedUploadedFolders\\'+str(uuid.uuid4()))
        self.response_data = {}
        self.face_client = FaceClient(AzureEndpoint, CognitiveServicesCredentials(AzureKey))
        self.faceids = []
        self.subject_obj = None

    def getStudentList(self):

        if self.validatedSubjectId():
            validatedUploadedfilesResp =  ValidateUploadedFiles().validatedFiles(self.upload_folder_path, self.request)
            
            if validatedUploadedfilesResp:
                self.saveSubjectInfoInSession()

                if self.generatedFaceId():

                    if self.getStudentsList():
                        self.saveSubjectInfoInSession()

                        shutil.rmtree(self.upload_folder_path)
                    
                        return self.response_data
                else:
                    shutil.rmtree(self.upload_folder_path)
                    return self.response_data
            else:
                return validatedUploadedfilesResp
        return self.response_data

    def validatedSubjectId(self):

        subject_id = self.request.POST.get('subject_id', False)

        if subject_id:
            try:
                self.subject_obj = Subject.objects.get(
                            faculty=Faculty.objects.get(email=self.request.user.username),
                            alpha_numeric_id = subject_id
                        )
                print(self.subject_obj)
                return True
            except Subject.DoesNotExist:
                print("subject not present")
                self.response_data["msg"] = "Invalid subject id"
                self.response_data["data"] = []
                self.response_data["status"] = "invalid"
        else:
            self.response_data["msg"] = "Subject not found"
            self.response_data["data"] = []
            self.response_data["status"] = "invalid"
        return False

    def generatedFaceId(self):

        for each_upload_image in os.listdir(self.upload_folder_path):
            
            with open(os.path.join(self.upload_folder_path, each_upload_image), 'rb') as f:
                try:

                    azure_detect_response = self.face_client.face.detect_with_stream(f, recognition_model='recognition_02', detection_model='detection_02', return_recognition_model=True)
                   
                    [ self.faceids.append( each_face_obj.face_id ) for each_face_obj in azure_detect_response ]
                    
                    print("faces ids ", self.faceids)
                except Exception as e:
                    print("exceptions in getting face ids ", e.args)
                    self.createAzureException(e)

                    return False
        return True

    def getStudentsList(self):

        azure_person_group_obj = self.subject_obj.azure_person_group


        no_of_blocks = math.ceil(len(self.faceids)/10)
        print("len of faceids",len(self.faceids))
        azure_person_ids = []
        block_size = 10
        block_start = 0
        block_end = block_size

        if no_of_blocks:
            
            for num in range( no_of_blocks ):
                
                face_list = self.faceids[block_start : block_end]
                print("num",num ,"face list", face_list, "azure person group id", azure_person_group_obj.person_group_id)
                try:
                
                    azure_persons_data = self.face_client.face.identify(
                        face_ids=face_list,person_group_id= azure_person_group_obj.person_group_id,
                        recognition_model="recognition_02"
                    )
                    print("azure identify response", azure_persons_data)
                    for e in azure_persons_data:
                        print(e.candidates)
                    [ azure_person_ids.append( x.candidates[0].person_id ) for x in azure_persons_data if x.candidates ]

                    block_start = block_end
                    block_end+=block_size
                except Exception as e:
                    print("azure identify exception")
                    print(e.args)
                    self.createAzureException(e)
                    return False
            
            print("azure person ids ", azure_person_ids)
            present_student_list = list( Student.objects.filter(azure_person_id__in=azure_person_ids, azure_person_group = azure_person_group_obj).values('full_name', 'enrollment_id') )
            absent_student_list = list( Student.objects.filter(azure_person_group = azure_person_group_obj).exclude(azure_person_id__in=azure_person_ids).values('full_name', 'enrollment_id') )
            
            self.response_data['msg']  = "success"
            self.response_data['data'] = {}
            self.response_data['data']['absent_students'] = absent_student_list
            self.response_data['data']['present_students'] = present_student_list
            self.response_data['status'] = "success"
            print("success")
            return True
        else:
            print("no content in photo")
            self.response_data["msg"] = "no content"
            self.response_data["data"] = []
            self.response_data["status"] = "success"


    def createAzureException(self, e):
        try:
            error_tuple = e.args
            print("error ", error_tuple)
            error_code = error_tuple[0].split('(')[1].split(')')
            
            if error_code[0]=="401":
                self.response_data["msg"] = "Please contact administrator"
                self.response_data["data"] = [error_code[1]]
                self.response_data["status"] = "error"
                
            elif error_code[0]=="OperationTimeOut":
                self.response_data["msg"] = "Request Timeout"
                self.response_data["data"] = []
                self.response_data["status"] = "error"

            elif error_code[0]=="400":
                self.response_data["msg"] = "Bad argument passed"
                self.response_data["data"] = [error_code[1]]
                self.response_data["status"] = "error"

            elif error_code[0]=="401":
                self.response_data["msg"] = "Please contact administrator"
                self.response_data["data"] = [error_code[1]]
                self.response_data["status"] = "error"
            
            elif error_code[0]=="403":
                self.response_data["msg"] = "Quota exceeded"
                self.response_data["data"] = []
                self.response_data["status"] = "error"

            elif error_code[0]=="429":
                self.response_data["msg"] = "Please try again after 1 minute"
                self.response_data["data"] = []
                self.response_data["status"] = "error"

            elif error_code[0]=="PersonGroupNotFound":
                self.response_data["msg"] = "not found"
                self.response_data["data"] = [error_code[1]]
                self.response_data["status"] = "error"
            
            elif error_code[0]=="PersonGroupTrainingNotFinished":
                self.response_data["msg"] = "Please try again after 1 minute"
                self.response_data["data"] = [error_code[1]]
                self.response_data["status"] = "error"

            else:
                self.response_data["msg"] = "unknown error"
                self.response_data["data"] = []
                self.response_data["status"] = "server_error"   

        except Exception as e:
            self.response_data["msg"] = "unknown error"
            self.response_data["data"] = []
            self.response_data["status"] = "server_error"



    def saveSubjectInfoInSession(self):
        
        token_data = TokenDecorder(self.request.session.get('token', False), self.request).decodeSessionToken(checking_type="user_type_checking")
        
        if token_data :

            subject_data = {
                "subject_alpha_id" : self.subject_obj.alpha_numeric_id
            }

            subject_encoded_data = jwt.encode(subject_data, JWTTokenSecretKey, algorithm='HS256')
            token_data["subject_token"] = subject_encoded_data.decode('utf-8')
            
            session_token = jwt.encode(token_data, JWTTokenSecretKey, algorithm='HS256')

            self.request.session['token'] = session_token.decode('utf-8')

            self.request.session.save()
            print("subject info saved in session")
        else:
            print("false given")

