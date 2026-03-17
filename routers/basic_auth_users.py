from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


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

def search_user(username: str):
    # print(username)
    # print(username in users_db)
   
    if username in users_db:
           return UserDB(**users_db[username])
    
print(f'\nNombre del usuario: {search_user("sofi").full_name}')
print(f'\nCorreo del usuario: {search_user("sofi").email}')
print(f'\nNombre del usuario: {search_user("test").full_name}')
print(users_db)
print(type(users_db))