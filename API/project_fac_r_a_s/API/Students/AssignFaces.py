import os
from django.core.files.storage import FileSystemStorage
import uuid
from GlobalsValues.globalValues import *
from API.models import *
from API.validators.ValidateUploadedFiles import ValidateUploadedFiles
import boto3
import shutil
from project_fac_r_a_s.settings import AWSSecretKey, AWSAccessKeyId, AzureKey, AzureEndpoint
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from API.Services.GetAzurePersonGroup import GetAzurePersonGroup

class AssignFaces:

    def __init__(self):
        super().__init__()
        
        self.upload_folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'TempCreatedUploadedFolders\\'+str(uuid.uuid4()))
        self.response_data = {}
        self.aws_boto3_client = boto3.client('s3', aws_access_key_id=AWSAccessKeyId, aws_secret_access_key=AWSSecretKey)
        self.s3_sub_folder_name = None
        self.student_object = None
        self.face_client = None

    def handlingUploadFiles(self, request):
        
        print("folder path ", self.upload_folder_path)

        validatedUploadedfilesResp =  ValidateUploadedFiles().validatedFiles(self.upload_folder_path, request)

        if validatedUploadedfilesResp["msg"] == "valid":

            if self.validateAzurePersonAndPersonGroup(request):
                
                if self.azureAssingFacesToPersonId():
                    self.response_data["msg"] = "uploaded successfully"
                    self.response_data["data"] = []
                    self.response_data["status"] = "success"

                    if self.train_group():
                        shutil.rmtree(self.upload_folder_path)
                        return self.response_data
                
            try:
                shutil.rmtree(self.upload_folder_path)
                print("deleted")
            except FileNotFoundError:      
                pass
            return self.response_data
        else:
            return validatedUploadedfilesResp
        
    def uploadImagesToS3Bucket(self, request):
        
        try:
            self.student_object = Student.objects.get(email=request.user.username)

            if not self.student_object.aws_s3_storage_folder_name:

                # not have s3 bucket. Hence create one
                self.student_object.aws_s3_storage_folder_name = str(uuid.uuid4())
                self.student_object.save()
            
            self.s3_sub_folder_name = self.student_object.aws_s3_storage_folder_name
            
            for each_upload_image in os.listdir(self.upload_folder_path):
                
                with open(os.path.join(self.upload_folder_path, each_upload_image), 'rb') as f:

                    self.aws_boto3_client.upload_fileobj(
                        f,
                        S3_UPLOAD_FACE_IMAGES_FOLDER,
                        self.student_object.aws_s3_storage_folder_name+"/"+each_upload_image,
                        ExtraArgs={'ACL': 'public-read'}
                    )
            return True
        except Exception as e:
            print(e)
            self.response_data["msg"] = "error during uploading"
            self.response_data["data"] = []
            self.response_data["status"] = "S3_error"
            return self.response_data

    def validateAzurePersonAndPersonGroup(self, request):

        self.student_object = Student.objects.get(email=request.user.username)

        self.face_client = FaceClient(AzureEndpoint, CognitiveServicesCredentials(AzureKey))

        # checking if Azure Person group has entry in database
        az_group_resp = GetAzurePersonGroup(batch_year=self.student_object.batch_year, branch=self.student_object.branch, college_obj=self.student_object.college).handleAzurePersonGroup()
        print(az_group_resp)
        if az_group_resp["status"] == "success":
            az_group = az_group_resp["data"]

            print("person group has entry in database", az_group)

            if self.student_object.azure_person_id:
                print("studnet has person id")
                return True
            else:
                # New student. Hence create person id in azure portal
                print("studnet does not have person id")
                print()
                try:
                    azure_person_object = self.face_client.person_group_person.create(az_group.person_group_id, name=self.student_object.full_name)
                    self.student_object.azure_person_id = azure_person_object.person_id
                    self.student_object.save()
                    print("studnet person id created")
                    return True

                except Exception as e:
                    print("error creating person id")
                    self.createAzureException(e, "person_group_exception")
        else:
            self.response_data["msg"] = "Error fetching person group"
            self.response_data["data"] = []
            self.response_data["status"] = "error"

    
    def createAzureException(self, e, exception_type):
        try:
            error_tuple = e.args
            print("error ", error_tuple)
            error_code = error_tuple[0].split('(')[1].split(')')
            
            if exception_type=="person_group_exception":
                
                if error_code[0]=="401":
                    self.response_data["msg"] = "Please contact administrator"
                    self.response_data["data"] = [error_code[1]]
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

                elif error_code[0]=="PersonGroupNotFound":
                    self.response_data["msg"] = "not found"
                    self.response_data["data"] = [error_code[1]]
                    self.response_data["status"] = "error"
                
                elif error_code[0]=="PersonGroupTrainingNotFinished":
                    self.response_data["msg"] = "Please try again after 1 minute"
                    self.response_data["data"] = [error_code[1]]
                    self.response_data["status"] = "error"

                elif error_code[0]=="429":
                    self.response_data["msg"] = "Please try again after 1 minute"
                    self.response_data["data"] = []
                    self.response_data["status"] = "error"

                else:
                    self.response_data["msg"] = "unknown error"
                    self.response_data["data"] = []
                    self.response_data["status"] = "server_error"   

            elif exception_type=="add_face_exception":
                
                if error_code[0]=="BadArgument":
                    self.response_data["msg"] = "bad argument"
                    self.response_data["data"] = [error_code[1]]
                    self.response_data["status"] = "error"
                
                elif error_code[0]=="401":
                    self.response_data["msg"] = "Please contact administrator"
                    self.response_data["data"] = [error_code[1]]
                    self.response_data["status"] = "error"
                
                elif error_code[0]=="QuotaExceeded":
                    self.response_data["msg"] = "Already added many faces"
                    self.response_data["data"] = [error_code[1]]
                    self.response_data["status"] = "error"
                
                elif error_code[0]=="PersonGroupNotFound":
                    self.response_data["msg"] = "not found"
                    self.response_data["data"] = [error_code[1]]
                    self.response_data["status"] = "error"
                
                elif error_code[0]=="Timeout":
                    self.response_data["msg"] = "Time out, Please try after some time again."
                    self.response_data["data"] = [error_code[1]]
                    self.response_data["status"] = "error"
                
                elif error_code[0]=="PersonGroupTrainingNotFinished":
                    self.response_data["msg"] = "Try after some time. Process is running"
                    self.response_data["data"] = [error_code[1]]
                    self.response_data["status"] = "error"
                
                elif error_code[0]=="429":
                    self.response_data["msg"] = "Please try again after 1 minute"
                    self.response_data["data"] = []
                    self.response_data["status"] = "error"

                elif error_code[0]=="InvalidImage":
                    self.response_data["msg"] = "multiple faces"
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


    def azureAssingFacesToPersonId(self):

        for each_upload_image in os.listdir(self.upload_folder_path):
                
            with open(os.path.join(self.upload_folder_path, each_upload_image), 'r+b') as f:

                try:
                    self.face_client.person_group_person.add_face_from_stream(self.student_object.azure_person_group.person_group_id, self.student_object.azure_person_id, f)
                    print("face added")
                except Exception as e:
                    print("error adding faces")
                    self.createAzureException(e, "add_face_exception")
                    print("error ", self.response_data)
                    return False
        print("all well")
        return True

    def train_group(self):

        azure_person_group_id = self.student_object.azure_person_group.person_group_id
        self.face_client.person_group.train(azure_person_group_id)
        print("trained")
        # while(True):
        #     try:
        #         training_status = self.face_client.person_group.get_training_status(azure_person_group_id)
        #         if (training_status.status is TrainingStatusType.succeeded):
        #             print("training status", training_status.status)
        #             return True
                
        #         elif (training_status.status is TrainingStatusType.failed):
        #             self.response_data["msg"] = "group not trained"
        #             self.response_data["data"] = [TrainingStatusType.failed]
        #             self.response_data["status"] = "training_error"    
        #     except Exception as e:
        #         self.createAzureException(e, "person_group_exception")
