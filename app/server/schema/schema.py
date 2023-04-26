from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    description: str
    price: float

class UpdateProduct(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    price: Optional[float]=None


class DisplaySeller(BaseModel):
    username:str
    email:str

    class Config:
        orm_mode = True
        
class DisplayProduct(BaseModel):
    name:str
    description:str
    seller: DisplaySeller

    class Config:
        orm_mode = True

class Seller(BaseModel):
    username:str
    email:str
    password:str

class Login(BaseModel):
    username:str
    password:str

