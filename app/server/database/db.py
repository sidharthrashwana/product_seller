from sqlalchemy import create_engine , engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.server.model import models
import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(

    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread":False
    }
)

session_local = sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base = declarative_base()

def connection_to_db():
    db = session_local()
    try :
        yield db
    finally:
        db.close()
    
def create_table():
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")