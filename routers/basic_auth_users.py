from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "123456"
    },

    "diego":{
        "username": "diego",
        "full_name": "Diego Hernández",
        "email": "diego@diego.com",
        "disabled": True,
        "password": "654321"
    },

    "test":{
        "username": "diego",
        "full_name": "Diego Hernández",
        "email": "diego@diego.com",
        "disabled": True,
        "password": "654321"        
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


async def current_user(token: str = Depends(oauth2)):
     user = search_user(token)
     if not user:
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED, 
               detail="Credenciales de autenticación inválidas", 
               headers={"WWW-Authenticate": "Bearer"})
     
     if user.disabled:
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, 
               detail="Usuario inactivo")
          
     return user
          
     
    
# print(f'\nNombre del usuario: {search_user("sofi").full_name}')
# print(f'\nCorreo del usuario: {search_user("sofi").email}')
# print(f'\nNombre del usuario: {search_user("test").full_name}')
# print(users_db)
# print(type(users_db))


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
     user_db = users_db.get(form.username)
     if not user_db:
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
     
     user = search_user_db(form.username)
     if not form.password == user.password:
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
     
     return {"access_token": user.username , "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
     return user