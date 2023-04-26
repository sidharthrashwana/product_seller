from sqlalchemy import Column , Integer, String,ForeignKey
from app.server.database.db import Base
from sqlalchemy.orm import relationship
#creating a table(or model)

#table with name 'Product' will be created
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    seller_id = Column(Integer,ForeignKey('sellers.id'))
    seller = relationship("Seller",back_populates="products")

class Seller(Base):
    __tablename__ = 'sellers'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    products = relationship("Product",back_populates="seller")