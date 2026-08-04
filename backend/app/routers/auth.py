from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..db import SessionLocal
from ..models_db import UserDB
from passlib.context import CryptContext
import jwt
import os
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
JWT_SECRET = os.getenv("JWT_SECRET", "devsecret")


class RegisterIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str


@router.post("/register")
def register(data: RegisterIn):
    session = SessionLocal()
    try:
        existing = session.query(UserDB).filter(UserDB.username == data.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="user exists")
        user = UserDB(username=data.username, hashed_password=pwd_context.hash(data.password))
        session.add(user)
        session.commit()
        return {"id": user.id, "username": user.username}
    finally:
        session.close()


@router.post("/token", response_model=TokenOut)
def token(form_data: RegisterIn):
    session = SessionLocal()
    try:
        user = session.query(UserDB).filter(UserDB.username == form_data.username).first()
        if not user or not pwd_context.verify(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="invalid credentials")
        token = jwt.encode({"sub": user.username}, JWT_SECRET)
        return {"access_token": token}
    finally:
        session.close()


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="invalid token")
        session = SessionLocal()
        user = session.query(UserDB).filter(UserDB.username == username).first()
        session.close()
        if not user:
            raise HTTPException(status_code=401, detail="user not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="invalid token")
