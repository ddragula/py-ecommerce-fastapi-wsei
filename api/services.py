from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
import xml.etree.ElementTree as ET
from .models import User, Basket, Order
from .schemas import UserCreate
from .database import SessionLocal

SECRET_KEY = "shouldbetakenfromenv" # Should be in .env file, but for demonstration purposes it's here, cause it's a demo project
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Create a basket for the user
    basket = Basket(user_id=db_user.id)
    db.add(basket)
    db.commit()
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def order_to_xml(order: Order) -> str:
    """Converts Order object to XML string"""
    order_elem = ET.Element("order")
    order_elem.set("id", str(order.id))
    order_elem.set("created_at", order.created_at.isoformat())

    items_elem = ET.SubElement(order_elem, "items")
    for item in order.items:
        item_elem = ET.SubElement(items_elem, "item")

        product_elem = ET.SubElement(item_elem, "product")
        product_elem.set("id", str(item.product.id))

        name_elem = ET.SubElement(product_elem, "name")
        name_elem.text = item.product.name

        price_elem = ET.SubElement(product_elem, "price")
        price_elem.text = str(item.price)

        quantity_elem = ET.SubElement(item_elem, "quantity")
        quantity_elem.text = str(item.quantity)
    return ET.tostring(order_elem, encoding="unicode")
