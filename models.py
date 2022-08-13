from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session
from database import Base
from schemas import UserCreate, ItemCreate

class User(Base):
    __tablename__= 'users'
    id= Column(Integer, primary_key= True, index= True)
    email= Column(String, unique= True, index= True)
    hashed_password= Column(String)
    is_active= Column(Boolean, default= True)
    items= relationship("Item", back_populates="owner")

    @staticmethod
    def get_by_id(db:Session, id:int):
        return db.query(User).filter(User.id==id).first()
    
    @staticmethod
    def get_by_email(db:Session, email:str):
        return db.query(User).filter(User.email==email).first()

    @staticmethod
    def get(db:Session, skip:int= 0, limit:int= 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create(db:Session, user:UserCreate):
        user_instance= User(email=user.email, hashed_password=user.password+'fake')
        db.add(user_instance)
        db.commit()
        db.refresh(user_instance)
        return user_instance


class Item(Base):
    __tablename__= 'items'
    id= Column(Integer, primary_key= True, index= True)
    title= Column(String, index= True)
    description= Column(String, index= True)
    owner_id= Column(Integer, ForeignKey('users.id'))
    owner= relationship('User', back_populates='items')

    @staticmethod
    def get(db:Session, skip:int= 0, limit:int= 100):
        return db.query(Item).offset(skip).limit(limit).all()

    @staticmethod
    def create(db:Session, item:ItemCreate, user_id:int):
        item_instance= Item(**item.dict(), owner_id= user_id)
        db.add(item_instance)
        db.commit()
        db.refresh(item_instance)
        return item_instance