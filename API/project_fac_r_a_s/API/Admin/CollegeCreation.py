from API.forms.NewCollegeForm import NewCollegeForm
from API.models import *
from GlobalsValues.globalValues import *


class CollegeCreation:

    def __init__(self):
        super().__init__()

        self.response_data = {}

    
    def handleCollegeCreation(self, request):
        print(request.POST)
        collegecreationform  =  NewCollegeForm(request.POST)
        
        if collegecreationform.is_valid():
            
            if self.addDetailsToDb(request)=="saved":
    
                self.response_data["msg"] = "created"
                self.response_data["data"] = list(College.objects.values())
                self.response_data["status"] = "success"
    
                print("data", self.response_data)

                return self.response_data
            else:
    
                self.response_data["msg"] = UNKNOWN_ERROR
                self.response_data["data"] = []
                self.response_data["status"] = "error"
                print("data", self.response_data)
    
                return self.response_data

        else:
    
            self.response_data["msg"] = "form error"
            self.response_data["data"] = [ collegecreationform.errors.as_json() ]
            self.response_data["status"] = "error"
            print("data", self.response_data)
    
            return self.response_data

    def addDetailsToDb(self, request):
        
        try:
            college_object = College.objects.create(
                                    college_name = request.POST['college_name'],
                                    college_code = request.POST['college_code'],
                                    gtu_afflicated = request.POST['gtu_afflicated'],
                                    domain = request.POST['domain']
                            )
            college_object.save()
            return "saved"
        except:
            return UNKNOWN_ERROR

