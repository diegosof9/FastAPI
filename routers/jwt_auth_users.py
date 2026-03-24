from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
# from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import bcrypt


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "e44ff49eaf0fa01f0a0684b7388c82f1ada3e579b370238646a97b8d0e9fc6e7"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# crypt = CryptContext(schemes=["bcrypt"])


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
        "disabled": False,
        "password": "$2a$12$H.DdsNgNcNXCwnxY4CUeu.LJ139TMUVJqAvL1KFLSagTr.9GUQZKK"
    },

    "test":{
        "username": "test",
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


def search_user(username: str):
    # print(username)
    # print(username in users_db)   
    if username in users_db:
           return User(**users_db[username])
    

async def auth_user(token: str = Depends(oauth2)):

     exception = HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED, 
          detail="Credenciales de autenticación inválidas", 
          headers={"WWW-Authenticate": "Bearer"})

     try:
          username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
          if username is None:
               raise exception

     except JWTError:
          raise exception
     
     return search_user(username)
    

async def current_user(user: User = Depends(auth_user)):
     
     if user.disabled:
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, 
               detail="Usuario inactivo")
          
     return user


@router.post("/loginjwt")
async def login(form: OAuth2PasswordRequestForm = Depends()):
     user_db = users_db.get(form.username)
     if not user_db:
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
     
     user = search_user_db(form.username)
       
     if not bcrypt.checkpw(form.password.encode(), user.password.encode()):
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
     
     access_token = {"sub": user.username, 
                     "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}

     return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/mejwt")
async def me(user: User = Depends(current_user)):
     return user