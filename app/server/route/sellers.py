from typing import Any,List
from fastapi import APIRouter, Body, Request,Depends,HTTPException,status,Response
import json
from pydantic import EmailStr
from app.server.utils.date_utils import get_current_timestamp
#JWT Implementation
from typing import Annotated, Union
from sqlalchemy.sql.functions import mode
from sqlalchemy.orm import Session
from app.server.schema import schema
from app.server.model import models
from app.server.database.db import engine,session_local,connection_to_db
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes = ["bcrypt"],deprecated="auto")

@router.post('/',summary='To create a seller',response_model=schema.DisplaySeller)
def create_seller(request:schema.Seller,
                  db:Session = Depends(connection_to_db)):
    hashed_password=pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username , 
                                email=request.email,
                                password=hashed_password)
    db.add(new_seller)
    db.commit()#insert new_product into db
    db.refresh(new_seller)#refresh the table
    return new_seller