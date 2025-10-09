from modules.users.model import UserModel
import jwt
import time
from dotenv import load_dotenv
import os

load_dotenv()

secret = os.getenv('JWT_SECRET')


def sign_jwt(user: UserModel):
    payload = {**user, 'expires': time.time() + 60 * 60 * 24}
    del payload['password']
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token_response(token)


def token_response(token: str):
    return {
        'access_token': token
    }


def decode_jwt(token: str):
    try:
        decoded_jwt = jwt.decode(token, secret, algorithms=['HS256'])
        if decoded_jwt['expires'] >= time.time():
            return decoded_jwt
        else:
            return None
    except:
        return {}
