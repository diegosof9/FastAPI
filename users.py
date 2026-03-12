from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name= "Sofi", surname= "Hernández", url= "https://diego.com", age= 13),
              User(id=2, name= "Diego", surname= "Hernández", url= "https://github.com/diegosof9", age= 39),
              User(id=3, name= "Diego", surname= "Hernández", url= "https://sofi.com", age= 39)]


@app.get("/usersjson")
async def usersjson():
    return [{"name": "Sofi", "surname": "Hernández", "url": "https://diego.com"},
            {"name": "Diego", "surname": "Hernández", "url": "https://sofi.com"}]


@app.get("/users")
async def users():
    return users_list


# Path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    

# Query
@app.get("/userquery/")
async def user(id: int):
    return search_user(id)

    
# def search_user(id: int):
#     user = filter(lambda user: user.id == id, users_list)
#     # print(user)
#     try:
#         # print(type(list(user)[0]))
#         return list(user)[0]
        
#     except:
#         return {"error":"No se ha encontrado el usuario"}


# POST
@app.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    # found_user = search_user(user.id)
    # print(found_user)
    # if type(search_user(user.id)) == User:
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
        # return {"error": "El usuario ya existe"}
    else:
        users_list.append(user)
        return user


# PUT
@app.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error":"No se ha actualizado el usuario"}
    
    else:
            return user


# DELETE
@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "No se ha eliminado el usuario"}
    

def search_user(id: int):
    for user in users_list:
        if user.id == id:
            return user
    return {"error":"No se ha encontrado el usuarioESTO ES UNA PRUEBA"}