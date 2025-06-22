from pydantic import BaseModel


class TokenBodyRequest(BaseModel):
    jwt_token: str