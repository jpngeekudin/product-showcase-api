from fastapi import APIRouter, Depends
from modules.products.model import ProductModel
from helpers.db import product_collection
from helpers.pagination import get_pagination, Pagination
from helpers.bson import parse_object_id
from bson import ObjectId
from helpers.jwt_bearer import JWTBearer

router = APIRouter(prefix="/products",
                   tags=['Product'], dependencies=[Depends(JWTBearer())])


@router.get('/')
async def get_all(pagination: Pagination = Depends(get_pagination)):
    products = await product_collection.find({}).skip(pagination.skip).limit(pagination.limit).to_list(length=None)
    data = parse_object_id(products)
    return {"success": True, 'data': data}


@router.get('/{id}')
async def get_by_id(id: str):
    product = await product_collection.find_one({'_id': ObjectId(id)})
    if product:
        return {'success': True, 'data': parse_object_id(product)}
    else:
        return {'success': False, 'message': "Not found"}


@router.post("/")
async def create(body: ProductModel):
    document = await product_collection.insert_one({'_id': ObjectId(), **body.model_dump()})
    return {"success": True, 'data': str(document.inserted_id)}


@router.put('/{id}')
async def update(id: str, body: ProductModel):
    document = await product_collection.update_one({'_id': ObjectId(id)}, body.model_dump())
    return {"success": True, 'data': document}


@router.delete('/{id}')
async def delete(id: str):
    document = await product_collection.delete_one({'_id': ObjectId(id)})
    return {"success": True, 'data': document.deleted_count}
