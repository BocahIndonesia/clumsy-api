from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
import time

models.Base.metadata.create_all(bind= engine)

app= FastAPI()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.middleware('http')
async def lucu(request:Request, call_next):
    start_time= time.time()
    response= await call_next(request)
    print('Processed time:', time.time() - start_time)
    return response

@app.post('/users/', response_model= schemas.User)
def create_user(user:schemas.UserCreate, db:Session= Depends(get_db)):
    user_exist= models.User.get_by_email(db= db, email= user.email)
    if user_exist:
        raise HTTPException(status_code= 400, detail= 'Email already registered')
    return models.User.create(db= db, user= user)

@app.get('/users/', response_model= list[schemas.User])
def get_users(skip:int =0, limit:int = 100, db:Session = Depends(get_db)):
    return models.User.get(db= db, skip= skip, limit= limit)

@app.get('/users/{id}', response_model= schemas.User)
def get_user_by_id(id:int, db:Session= Depends(get_db)):
    u= models.User.get_by_id(db= db, id= id)
    if u is None:
        raise HTTPException(status_code= 404, detail= 'user is not found')
    return u

@app.post('/users/{user_id}/items/', response_model= schemas.Item)
def create_item(user_id:int, item:schemas.ItemCreate, db:Session= Depends(get_db)):
    return models.Item.create(db= db, item= item, user_id= user_id)

@app.get('/items/', response_model= list[schemas.Item])
def get_items(skip:int= 0, limit:int= 100, db:Session= Depends(get_db)):
    return models.Item.get(db= db, skip= skip, limit= limit)
