from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from helpers.jwt_bearer import JWTBearer
from enum import Enum
import os

upload_dir = 'upload'


class FileCategory(str, Enum):
    PRODUCT_IMAGE = 'product_image'


router = APIRouter(
    prefix='/files', tags=['File'])


@router.post('/upload', dependencies=[Depends(JWTBearer())])
async def upload_file(type: FileCategory, file: UploadFile = File()):
    directory = os.path.join(upload_dir, type)
    os.makedirs(directory, exist_ok=True)

    identifier = os.path.join(type, file.filename)
    file_path = os.path.join(upload_dir, identifier)

    with open(file_path, 'wb') as buffer:
        while content := await file.read(1024 * 1024):
            buffer.write(content)

    return {"success": True, "data": identifier}


@router.get('/get')
async def get_file(path: str):
    complete_path = os.path.join(upload_dir, path)
    return FileResponse(complete_path)
