from pydantic import BaseModel, Field
import time


class UserModel(BaseModel):
    username: str
    password: str
    fullname: str
    phone: str
    email: str
    image: str
    status: bool
    created_at: int = Field(time.time() * 1000)
