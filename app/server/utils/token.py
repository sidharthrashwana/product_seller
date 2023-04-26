import os
from jose import jwt,JWTError
from dotenv import load_dotenv
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from passlib.context import CryptContext
from app.server.schema.token import TokenData
load_dotenv()

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))

pwd_context = CryptContext(schemes = ["bcrypt"],deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate/login")

def generate_token(data:dict):
    to_encode = data.copy()
    #get current time and add expiry time to it
    expire = datetime.utcnow() +  timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,JWT_SECRET_KEY,algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail ="Invalid auth credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY,algorithms=[JWT_ALGORITHM])
        username:str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

        