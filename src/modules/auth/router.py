from fastapi import APIRouter
from modules.auth.model import LoginIn
from helpers.db import user_collection
from helpers.jwt import sign_jwt
import hashlib

router = APIRouter(prefix='/auth')


@router.post('/login', tags=['Auth'])
async def login(body: LoginIn):
    hashed_password = hashlib.md5(body.password.encode()).hexdigest()
    print(hashed_password)
    user = await user_collection.find_one({"username": body.username, 'password': hashed_password}, {'_id': 0})
    if user:
        signed = sign_jwt(user)
        return {"success": True, "data": signed}
    else:
        return {"success": False, "message": 'Invalid login'}


@router.post('/logout', tags=['Auth'])
async def logout():
    return {"message": "Logout"}
