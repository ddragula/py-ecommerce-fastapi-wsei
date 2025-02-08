from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..database import SessionLocal
from ..models import User as UserModel, Basket, Order
from ..services import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, create_user
from ..schemas import User as UserSchema, UserCreate

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
