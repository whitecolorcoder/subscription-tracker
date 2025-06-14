import datetime
from src.config import Settings
from src.models.users import User
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from typing import Tuple

class JWTService:
    def __init__(self, config: Settings):
        self.config = config
    
    def create_jwt(self, user_id: int)-> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # expires in 1 hour
        }
        token = jwt.encode(payload, self.config.SECRET_KEY, algorithm="HS256")
        return token
    
    def check_jwt(self, token) -> int | Tuple[str, int]:
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=["HS256"])
            return payload['user_id']
        except ExpiredSignatureError:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=["HS256"] ,options={"verify_exp": False})
            new_token = self.create_jwt(payload['user_id']) 
            return new_token, payload['user_id']
        except InvalidTokenError:
            raise InvalidTokenError
            
