import jwt
from project_fac_r_a_s.settings import JWTTokenSecretKey
from API.models import Faculty
from GlobalsValues.globalValues import *


class TokenDecorder:

    def __init__(self, token, request):
        super().__init__()
        self.token = token
        self.request = request

    def decodeSessionToken(self, checking_type=None):
        
        if self.token:
            try:
                decoded_data = jwt.decode(
                    self.token,
                    JWTTokenSecretKey,
                    algorithm='HS256'
                )
                print("token data", decoded_data)
                return decoded_data
            except jwt.exceptions.ExpiredSignatureError:
                print("token expired")

                if checking_type == "user_type_checking":
                    
                    encoded_data = {
                        "user_type": HOD if Faculty.objects.get(email= self.request.user.username).faculty_type_hod else ASSISTANT_PROFESSOR
                    }

                    session_enocoded_token = jwt.encode(
                        encoded_data,
                        JWTTokenSecretKey,
                        algorithm="HS256"
                    )
                    self.request.session["token"] = session_enocoded_token.decode('utf-8')
                    return encoded_data
                else:
                    print("none")
                    return "expired"
        else:
            False