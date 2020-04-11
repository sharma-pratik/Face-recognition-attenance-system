from API.models import *
from django.db.models import Q
import uuid
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from project_fac_r_a_s.settings import AWSSecretKey, AWSAccessKeyId, AzureKey, AzureEndpoint


class GetAzurePersonGroup:

    def __init__(self, batch_year, branch, college_obj):

        self.branch = branch
        self.batch_year = batch_year
        self.college_obj = college_obj
        self.face_client = None
        self.azure_person_group_obj = None
        self.response_data = {}
    
    def handleAzurePersonGroup(self):
        print("in handling of person group", self.branch, self.batch_year, self.college_obj)
        self.gettingOrCreatingAzureGroup()
        print("final response ", self.response_data)
        return self.response_data

    def gettingOrCreatingAzureGroup(self):

        az_group = AzurePersonGroup.objects.filter(
            Q(branch=self.branch), Q(batch_year=self.batch_year), Q(college= self.college_obj) 
        )
        print(az_group)
        if az_group:
            print("group exists ", az_group)
            self.azure_person_group_obj = az_group[0]
            self.response_data["msg"] = "success"
            self.response_data["data"] = self.azure_person_group_obj
            self.response_data["status"] = "success"

        else:
            print("group not exists")

            if self.createAzurePersonGroup() == "created":
                print("group created")

                # if self.trainAzureGroup():
                print("training success")
                self.azure_person_group_obj.save()
                self.assignSubjectToAzgroup()

                self.response_data["msg"] = "success"
                self.response_data["data"] = self.azure_person_group_obj
                self.response_data["status"] = "success"
                
    def createAzurePersonGroup(self):
        
        self.face_client = FaceClient(AzureEndpoint, CognitiveServicesCredentials(AzureKey))

        try:
            az_person_group = AzurePersonGroup(
                person_group_id = str(uuid.uuid4()),
                person_group_name = self.college_obj.college_name+"_"+ self.branch +"_"+self.batch_year+"_batch",
                college = self.college_obj,
                batch_year = self.batch_year,
                branch = self.branch
            )   

            print(az_person_group.person_group_id)

            self.face_client.person_group.create(
                person_group_id=az_person_group.person_group_id,
                name=az_person_group.person_group_name,
                recognition_model="recognition_02" 
            )
            self.azure_person_group_obj = az_person_group
            return "created"
            
        except Exception as e:
            print("exception in creating group")
            self.createAzureException(e)

    def createAzureException(self, e ):
        try:
            error_tuple = e.args
            print("error ", error_tuple)
            error_code = error_tuple[0].split('(')[1].split(')')
            print(error_code)
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

            elif "HTTPSConnectionPool" in error_code[0]:
                self.response_data["msg"] = "Please check network"
                self.response_data["data"] = []
                self.response_data["status"] = "network_error"

            else:
                self.response_data["msg"] = "unknown error"
                self.response_data["data"] = []
                self.response_data["status"] = "server_error"   

        except Exception as e:
            self.response_data["msg"] = "unknown error"
            self.response_data["data"] = []
            self.response_data["status"] = "server_error"
    
    def assignSubjectToAzgroup(self):

        Subject.objects.create(
            subject_name = "Math 3",
            branch = self.branch,
            subject_code = 210014,
            faculty = Faculty.objects.get(pk=1),
            college = self.college_obj,
            azure_person_group = self.azure_person_group_obj,
        )
        print("subject created ")

    def trainAzureGroup(self):
        
        azure_person_group_id = self.azure_person_group_obj.person_group_id
        print(azure_person_group_id)
        self.face_client.person_group.train(azure_person_group_id)
        
        while(True):
            try:
                print("training")
                training_status = self.face_client.person_group.get_training_status(azure_person_group_id)
                print("status ", training_status, training_status.status)
                if (training_status.status is TrainingStatusType.succeeded):
                    print("training status", training_status.status)
                    return True
                
                elif (training_status.status is TrainingStatusType.failed):
                    self.response_data["msg"] = "group not trained"
                    self.response_data["data"] = [TrainingStatusType.failed]
                    self.response_data["status"] = "training_error"
            except Exception as e:
                print("exception in training ", e)
                self.createAzureException(e)
