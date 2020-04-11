from API.models import *

class FetchSubjectsInfo:

    def __init__(self, request):
        super().__init__()
        self.request = request
        self.response_data = {}
        

    def fetchSubjects(self):

        try:
            currentUser =  Faculty.objects.get(email = self.request.user.username )

            subject_info = list (
                    Subject.objects.filter(
                    faculty = currentUser
                ).values('subject_name', 'subject_code', 'alpha_numeric_id')
            )

            for subj in subject_info:
                print(subj)
                subj["name"]= subj.pop('subject_name')
                subj["code"]= subj.pop('subject_code')
                subj["id"] = subj.pop('alpha_numeric_id')

            self.response_data["msg"] = "subjects information"
            self.response_data["data"] = subject_info
            self.response_data["status"] = "success"
        
        except Exception as e:
            print(e)
            self.response_data["msg"] = "unknown error"
            self.response_data["data"] = []
            self.response_data["status"] == "error"
        
        return self.response_data