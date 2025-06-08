from pydantic import BaseModel, Email
from auth import AuthX, AuthConfig
from fastapi import FastAPI

app = FastAPI()

config = AuthConfig()
config.JWT_JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token_cookie"
config.JWT_TOKEN_LOCATION = ["headers"]

security = AuthX(config=config)

class GetEmailandPassword(BaseModel):
    email: Email 
    password : str

@app.post("/login")
def login(body:GetEmailandPassword):
    if 
    


@app.get("/protected")
def protected():
    ...
