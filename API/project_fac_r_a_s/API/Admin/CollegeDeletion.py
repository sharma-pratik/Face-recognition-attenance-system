from API.models import *
from GlobalsValues.globalValues import *
from django.shortcuts import get_object_or_404

class CollegeDeletion:

    def __init__(self):
        super().__init__()
        self.response_data = {}


    def handlingCollegeDeletion(self, request):

        college_code = request.POST.get('college_code', False)

        if college_code and college_code.isnumeric():
            
            # check if college code exists
            try:
                
                college_obj = College.objects.get(college_code=college_code)

                college_obj.delete()
                self.response_data['msg'] = DELETED
                self.response_data['data'] = []
                self.response_data['status'] = "success"
                return self.response_data

            except College.DoesNotExist:

                self.response_data["msg"] = "not found"
                self.response_data["data"] = [college_code]
                self.response_data["status"] = "error"
                return self.response_data
        
        else:
            self.response_data["msg"] = "invalid input"
            self.response_data["data"] = []
            self.response_data["status"] = "error"
            return self.response_data


