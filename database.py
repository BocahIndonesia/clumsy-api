import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
engine= create_engine(f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_DATABASE")}', echo=True)
SessionLocal= sessionmaker(autocommit= False, autoflush= False, bind= engine)
Base= declarative_base()