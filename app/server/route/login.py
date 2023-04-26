from fastapi import APIRouter,Depends,status,HTTPException
from app.server.database.db import engine,session_local,connection_to_db
from app.server.model import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.server.schema import schema
from app.server.utils import token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter()

pwd_context = CryptContext(schemes = ["bcrypt"],deprecated="auto")


@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(connection_to_db)):
    seller = db.query(models.Seller).filter(
        models.Seller.username == request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Username not found.")
    if not pwd_context.verify(request.password,seller.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="invalid password")
    #pass username and get access token
    access_token=token.generate_token(
        data = {"sub":seller.username}
    )
    return {"access_token":access_token , "token_type":"bearer"}