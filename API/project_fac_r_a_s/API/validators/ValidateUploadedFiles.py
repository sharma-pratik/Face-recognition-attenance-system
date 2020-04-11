from django.core.files.storage import FileSystemStorage
from GlobalsValues.globalValues import *
import uuid, shutil, os


class ValidateUploadedFiles:

    def __init__(self):
        super().__init__()

        self.valideFileExtension = ['JPG', 'jpg', 'PNG', 'png', 'JPEG', 'jpeg']
        self.response_data = {}

    def validatedFiles(self, folder_path, request):
        
        if 'upload-images' in request.FILES and request.FILES.getlist('upload-images'):
            os.makedirs(folder_path)
            print("folder created ", folder_path)
            
            uploaded_files = request.FILES.getlist('upload-images')

            for each_file in uploaded_files:
                
                file_extension = each_file.name.split('.',)[-1]

                # checking valid file extension
                if file_extension in self.valideFileExtension:
                
                    fs = FileSystemStorage(location=folder_path)
                    fs.save(str(uuid.uuid4())+"."+file_extension, each_file)
            
                else:
                    print("invalid uploaded files")
                    self.response_data["msg"]= INVALID_FORMAT
                    self.response_data["data"] = []
                    self.response_data["status"] = "invalid"
                    shutil.rmtree(folder_path)
                    # deleted created folder 
            self.response_data["msg"]  = "valid"
            self.response_data["data"]  = []
            self.response_data["status"]  = "valid"
                
        else:
            print("invalid uploaded files")
            self.response_data["msg"]= "invalid request type"
            self.response_data["data"] = []
            self.response_data["status"] = "invalid"

        return self.response_data