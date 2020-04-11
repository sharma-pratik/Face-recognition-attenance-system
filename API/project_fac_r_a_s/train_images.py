import asyncio
import io
import glob
import os
import requests
import sys
import time
import uuid
# import names
import json
import boto3
from PIL import Image 
import requests
import base64
from urllib.parse import urlparse
from io import BytesIO

from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
import uuid
import http.client, urllib.request, urllib.parse, urllib.error, base64

# headers = {
#     # Request headers
#     'Content-Type': 'application/json',
#     'Ocp-Apim-Subscription-Key': 'acd260c437d34b3f82cbf62bf31a2faf',
# }

# params = urllib.parse.urlencode({
# })

# try:
#     conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
#     conn.request("PUT", "/face/v1.0/persongroups/students/?%s" % params, "{body}", headers)
#     response = conn.getresponse()
#     data = response.read()
#     print(data)
#     conn.close()
# except Exception as e:
#     print("[Errno {0}] {1}".format(e.errno, e.strerror))

# exit()
person_ids = []
PERSON_GROUP_ID = "group_one"
SECOND_PERSON_GROUP = "second_person_group"
KEY =  "acd260c437d34b3f82cbf62bf31a2faf"
ENDPOINT ="https://westcentralus.api.cognitive.microsoft.com/face/v1.0/"

identified_ids = []

persons_data = []

def create_person_group():

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': "acd260c437d34b3f82cbf62bf31a2faf"
    }

    # params = {
    #     "personGroupId" : "student"
    # }

    url = ENDPOINT+"persongroups/studentss"

    body = {
        "name": "student_group",
        'recognitionModel' : 'recognition_02'
    }
    response = requests.put(url, headers=headers, json=body)
    print(response)



def get_training_status(id):

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': "acd260c437d34b3f82cbf62bf31a2faf"
    }

    url = ENDPOINT+"persongroups/"+id+"/training"

    response = requests.get(url, headers=headers)
    print(json.loads(response.text))


def list_person_groups():

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': "acd260c437d34b3f82cbf62bf31a2faf"
    }
    url = ENDPOINT+"/persongroups"

    response = requests.request('GET',url,headers=headers)
    print(json.loads(response.text))

def create_person(person_group_id):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY
    }

    # s3_client = boto3.client('s3', aws_access_key_id='AKIAJ6KV33T2DHT2YUUA', aws_secret_access_key='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')
    # s3_resource = boto3.resource('s3', aws_access_key_id='AKIAJ6KV33T2DHT2YUUA', aws_secret_access_key='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')


    # bucket = s3_resource.Bucket('studentsimages')
    # number_of_user = 0
    
    # for image_object in bucket.objects.all():
    #     number_of_user =  number_of_user+1
    #     user_name = names.get_full_name()
    # image_url =  "https://studentsimages.s3.amazonaws.com/"+image_object.key

        # person_data = {
        #     "person_id":"",
        #     "id":number_of_user,
        #     "name": user_name
        # }

    body = {
        "name":"parth patel 2"
    }

    create_person_url = ENDPOINT+"/persongroups/"+person_group_id+"/persons"

    user_person_id = json.loads( requests.request('POST', create_person_url, json=body, headers=headers).text)['personId']

    print("personl id= ",user_person_id)

   
def delete_person_group(person_group_id):

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY
    }

    url = ENDPOINT+"/persongroups/"+person_group_id
    response = requests.request("DELETE", url, headers=headers)
    print(response)

def list_persons(person_group_id):
    
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY
    }

    url = ENDPOINT+"persongroups/"+person_group_id+"/persons"
    print(url)
    response = requests.request('GET', url, headers=headers)
    print(response)
    data = json.loads(response.text)
    print(data) 

def train_person_group(person_group_id):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY
    }

    url = ENDPOINT+"/persongroups/"+person_group_id+"/train"
    print(url)

    response = requests.request('POST', url, headers=headers)
    print(response)

def detect_faceID(image_url):
    
    face_ids = []
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': KEY,
    }

    params = {
        'returnFaceId': 'true',
        'recognitionModel' : 'recognition_01',
        'returnRecognitionModel': True
    }

    body = {'url': image_url}
    
    response = requests.request('POST', ENDPOINT+"/detect", json=body, data=None, headers=headers, params=params)
    detected_data = json.loads(response.text)
    print(detected_data)
    # response = requests.get(image_url)
    # img = Image.open(BytesIO(response.content))
    # draw = ImageDraw.Draw(img)

    # for face in detected_data:
    #     draw.rectangle(getRectangle(face), outline='red')

    # img.show()

    face_ids = list(map(lambda x:x['faceId'], detected_data))

    return face_ids

def identify_faces(facesids, person_group_id):
    
    response = requests.request('POST', ENDPOINT+"identify", json={"faceIds":facesids,"personGroupId" : person_group_id, "maxNumOfCandidatesReturned":30}, headers={'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': KEY}, params = {'recognitionModel' : 'recognition_01', 'detectionModel' : 'detection_01'})
    response = json.loads(response.text)
    print("response= ", response)


def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    right = left + rect['width']
    bottom = top + rect['height']
    
    return ((left, top), (right, bottom))

def show_person_group_person_info(person_group_id, person_id):

    headers = {
        'Content-Type': 'application/json',
        "Ocp-Apim-Subscription-Key": KEY
    }

    url = "{}/persongroups/{}/persons/{}".format(ENDPOINT, person_group_id, person_id)
    print(url)
    res = requests.request('GET', url, headers=headers)
    print(json.loads(res.text))

def delete_persistent_face_ids(person_group_id, person_id, persistent_face_id):
    
    headers = {
        "Ocp-Apim-Subscription-Key": KEY
    }

    url = "{}/persongroups/{}/persons/{}/persistedFaces/{}".format(ENDPOINT, person_group_id, person_id, persistent_face_id)
    print(url)
    res = requests.request('DELETE', url, headers=headers)
    print(res)

def add_face_to_person(person_group_id, person_id, url):

    headers = {
        'Content-Type': 'application/json',
        "Ocp-Apim-Subscription-Key": KEY
    }

    params = {
        'detectionModel':'detection_01'
    }
    
    body={
        'url': url
    }
    add_face_url = ENDPOINT+"persongroups/{}/persons/{}/persistedFaces/".format(person_group_id, person_id)
    print(add_face_url)
    res = requests.request('POST', add_face_url, headers=headers, json=body, params=params)
    print(json.dumps(res.text))

def get_person_group_info(person_group_id):


    headers = {
        "Ocp-Apim-Subscription-Key": KEY
    }
    url = ENDPOINT+"persongroups/{}".format(person_group_id)
    params = {
        "returnRecognitionModel":True
    }
    res = requests.request('GET', url, headers=headers, params=params)
    print(json.dumps(res.text))


# create_person(person_group_id="r_02_model_person_group")
# # add_face_to_person(person_group_id="r_02_model_person_group", person_id="8c93ed58-c4e6-4ec6-bc91-7421f27f5d8e", url="https://studentsimages.s3.amazonaws.com/parth.jpg")
# train_person_group(person_group_id = "2b601fbf-0eac-4aaf-b361-24ba3f7c4ec1")
# train_person_group(person_group_id = "334e3446-d047-4900-b8f1-1a38ddc1d72e")


# facesids = detect_faceID(image_url="https://studentsimages.s3.amazonaws.com/unnamed+(1).jpg")
# print(facesids)
# facesids = ['feb2b6a6-163e-4ecc-b7ad-55122a03c1ab', '1f41bca1-e823-4ab1-a044-1b92d5e364b1', 'c18a6554-74f7-4601-9f65-982367ecf599', '6bbade46-b725-4528-8548-7dca2b79a710', '71cbecf5-4134-4ea1-86a2-fef7a3891bb7', 'd0c90d05-ee25-42ea-b2ab-b6e87496efb8']
# identify_faces(facesids=facesids, person_group_id="r_02_model_person_group")
# delete_persistent_face_ids(person_group_id="r_02_model_person_group", person_id="1645763f-aea2-403c-9856-8a1ca5252e0f" , persistent_face_id="6dddcbbc-608a-4130-9d4e-424b312f016c")
# show_person_group_person_info(person_group_id=PERSON_GROUP_ID, person_id="32d925cd-75f6-4101-bb21-e1a7ab0a8403" )
# list_person_groups()
# list_persons(person_group_id=PERSON_GROUP_ID)
# delete_person_group(person_group_id="9d9e1ee8-e640-472d-b666-d7b22a28d96a")
# delete_person_group(person_group_id="f69e77db-84ec-4506-962b-bda1dfcc1f93")
get_training_status(id="06eaf63a-b25f-45ae-bfff-9d3824a53d57")
train_person_group(person_group_id="06eaf63a-b25f-45ae-bfff-9d3824a53d57")
list_person_groups()
# print(PERSON_GROUP_ID)
# list_person_groups()
# create_person(person_group_id="24f04541-d87e-4c3d-85c3-e960e80662ba")
# list_persons(person_group_id="24f04541-d87e-4c3d-85c3-e960e80662ba")

# # let me down slowly 
# detect_faceID(image_url="https://www.geo.tv/assets/uploads/updates/2020-04-04/280940_2226210_updates.jpg")



# get_person_group_info(person_group_id='r_02_model_person_group')