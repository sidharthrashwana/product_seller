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
from app.server.utils.token import generate_token,get_current_user
router = APIRouter()

try:
    models.Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")

@router.get('/',summary='To get all products',
            response_model=List[schema.DisplayProduct])
def products(current_user:schema.Seller = Depends(get_current_user),
             db:Session = Depends(connection_to_db)):
    products = db.query(models.Product).all()
    return products

@router.get('/{id}',summary='To get specific product by id',
            response_model=schema.DisplayProduct)
def product_by_id(id:int , response:Response,db:Session = Depends(connection_to_db)):
    specific_product = db.query(models.Product).filter(models.Product.id == id ).first()
    if not specific_product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail='Product not found')
    return specific_product


@router.delete('/{id}',summary='To delete specific product by id')
def product_by_id(id:int , db:Session = Depends(connection_to_db)):
    specific_product = db.query(models.Product).filter(models.Product.id == id ).delete(
        synchronize_session=False)
    db.commit()
    return {'product deleted'}

@router.put('/{id}',summary='To update specific product by id')
def product_by_id(id:int ,request: schema.UpdateProduct, db:Session = Depends(connection_to_db)):
    specific_product = db.query(models.Product).filter(models.Product.id == id )
    if not specific_product.first():
        pass
    specific_product.update(request.dict() )
    db.commit()
    return {'product updated'}

@router.post('/', summary='To create a product',status_code=status.HTTP_201_CREATED)
async def add(request: schema.Product,
              db:Session = Depends(connection_to_db)):
    new_product = models.Product(name=request.name , 
                                 description=request.description,
                                 price=request.price,
                                seller_id=1)
    db.add(new_product)
    db.commit()#insert new_product into db
    db.refresh(new_product)#refresh the table
    return request