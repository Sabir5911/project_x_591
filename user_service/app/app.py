import datetime
from fastapi import FastAPI, Request, Response, HTTPException, status, Depends
from sqlmodel import Session,SQLModel
import psycopg2
from typing import Annotated
from models import user_data
from engine import get_session,engine
from crud import get_all_users, get_user_by_id, create_user, check_user_credentials
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta,datetime
from jose import JWTError, jwt
import uvicorn

app: FastAPI = FastAPI()


OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="login")


SQLModel.metadata.create_all(engine)

SECRET_KEY="ASkaslksaladjlakdjalksda"
ALGORITHM="HS256"



def create_token(id,email,name,password,expires:timedelta):
    expire=datetime.utcnow()+expires
    to_encode={"exp":expire,"username":name,"pass":password,"email":email,"id":id}
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None




@app.get("/",tags=["Root"])
def read_root():
    return {"message": "Hello World"}



@app.post("/login",tags=["Login"])
def loginForm(form_data:Annotated[OAuth2PasswordRequestForm,Depends(OAuth2PasswordRequestForm)],session: Session = Depends(get_session)):
    
    user=check_user_credentials(session=session,username=form_data.username,password=form_data.password)
    if user is False:
        raise HTTPException(status_code=404, detail="User not found")
    
    token=create_token(user.id,user.email,user.username,user.password,timedelta(minutes=30))

    return {"access_token":token,"token_type":"bearer"}



@app.get("/users", response_model=list[user_data])
def read_all_users(session: Session = Depends(get_session), token: str = Depends(OAuth2PasswordBearer)):
    users = get_all_users(session=session)
    return users



@app.get("/users/{user_id}", response_model=user_data)
def read_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users",tags=["Sign Up"], response_model=user_data)
def create_new_user(user: user_data, session: Session = Depends(get_session)):
    user = create_user(session=session, user=user)
    return user


@app.get("/token",tags=["Token"])
def token(token: str = Depends(OAuth2PasswordBearer)):
    return {"token": token}


if __name__ == "__main__":
    uvicorn.run(app, host="")

