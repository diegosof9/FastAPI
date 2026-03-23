from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "sofi":{
        "username": "sofi",
        "full_name": "Sofía Hernández Raga",
        "email": "sofi@sofi.com",
        "disabled": False,
        "password": "$2a$12$QjEPVxOdNw7o55kHTW2ozORpIwuBLUP4Z7GKxW.KaDEDMXak.QMZ2"
    },

    "diego":{
        "username": "diego",
        "full_name": "Diego Hernández",
        "email": "diego@diego.com",
        "disabled": True,
        "password": "$2a$12$H.DdsNgNcNXCwnxY4CUeu.LJ139TMUVJqAvL1KFLSagTr.9GUQZKK"
    },

    "test":{
        "username": "diego",
        "full_name": "Diego Hernández",
        "email": "diego@diego.com",
        "disabled": True,
        "password": "$2a$12$6ZpFx0Owfg0eCUD9wX/ZXeHUm48VHaP/SgbY/Dztc9uO3n1K83h2i"        
    }
    
}


def search_user_db(username: str):
    # print(username)
    # print(username in users_db)   
    if username in users_db:
           return UserDB(**users_db[username])


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
     user_db = users_db.get(form.username)
     if not user_db:
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
     
     user = search_user_db(form.username)
       
     if not crypt.verify(form.password, user.password):
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
     
     expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)

     return {"access_token": user.username , "token_type": "bearer"}