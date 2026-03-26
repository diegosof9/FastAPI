from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())


# Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Query
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

    
# def search_user(id: int):
#     user = filter(lambda user: user.id == id, users_list)
#     # print(user)
#     try:
#         # print(type(list(user)[0]))
#         return list(user)[0]
        
#     except:
#         return {"error":"No se ha encontrado el usuario"}


# POST
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    # found_user = search_user(user.id)
    # print(found_user)
    # if type(search_user(user.id)) == User:
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    #     # return {"error": "El usuario ya existe"}
    # else:

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    
    return User(**new_user)


# PUT
@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)    
    except:
        return {"error":"No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))



# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}
    

def search_user(field: str, key): 
    print("Buscando:", {field: key})
    try:
        user = db_client.local.users.find_one({field: key})
        print("Buscando:", {field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}