from fastapi import APIRouter, Depends
from bson import ObjectId
from helpers.db import user_collection
from helpers.pagination import get_pagination, Pagination
from helpers.bson import parse_object_id
from modules.users.model import UserModel
from helpers.jwt_bearer import JWTBearer
import hashlib

router = APIRouter(
    prefix='/user', tags=["User"], dependencies=[Depends(JWTBearer())])


@router.get('')
async def get_users(pagination: Pagination = Depends(get_pagination)):
    total = await user_collection.count_documents({})
    documents = await user_collection.find({}).skip(pagination.skip).limit(pagination.limit).to_list()
    data = parse_object_id(documents)
    return {"success": True, "data": data, 'metadata': {'total': total}}


@router.get('/{id}')
async def get_user_by_id(id: str):
    document = await user_collection.find_one({'_id': ObjectId(id)})
    data = parse_object_id(document)
    return {"success": True, "data": data}


@router.post('')
async def create(body: UserModel):
    hashed_password = hashlib.md5(body.password.encode()).hexdigest()
    document = await user_collection.insert_one({'_id': ObjectId(), **body.model_dump(), 'password': hashed_password})
    return {"success": True, 'data': str(document.inserted_id)}


@router.put('/{id}')
async def update_user(id: str, body: UserModel):
    document = await user_collection.update_one({'_id': ObjectId(id)}, {'$set': body.model_dump()})
    return {"success": True, "data": document.raw_result}


@router.delete('/{id}')
async def delete_user(id: str):
    document = await user_collection.delete_one({'_id': ObjectId(id)})
    return {"success": True, 'data': document.deleted_count}
