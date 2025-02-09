from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


# ====================
# User schemas

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ====================
# Product schemas

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ====================
# Basket schemas

class BasketItem(BaseModel):
    product: Product
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class Basket(BaseModel):
    id: int
    items: List[BasketItem] = []

    model_config = ConfigDict(from_attributes=True)


# ====================
# Order schemas

class OrderItem(BaseModel):
    product: Product
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)

class Order(BaseModel):
    id: int
    created_at: datetime
    items: List[OrderItem] = []

    model_config = ConfigDict(from_attributes=True)
