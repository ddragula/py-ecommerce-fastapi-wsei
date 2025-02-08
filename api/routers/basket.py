from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from ..database import SessionLocal
from ..models import Basket, BasketItem, Product, User
from ..services import SECRET_KEY, ALGORITHM
from ..schemas import Basket as BasketSchema

router = APIRouter(
    prefix="/api/basket",
    tags=["basket"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


class AddToBasket(BaseModel):
    product_id: int
    quantity: int = 1


@router.post("/add")
def add_to_basket(item: AddToBasket,
                  current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not basket:
        # Create basket if not exists
        basket = Basket(user_id=current_user.id)
        db.add(basket)
        db.commit()
        db.refresh(basket)
    # Chcek if item is already in basket
    basket_item = db.query(BasketItem).filter(
        BasketItem.basket_id == basket.id,
        BasketItem.product_id == item.product_id
    ).first()
    if basket_item:
        basket_item.quantity += item.quantity
    else:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        basket_item = BasketItem(
            basket_id=basket.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(basket_item)
    db.commit()
    return {"message": "Item added to basket"}


@router.get("/", response_model=BasketSchema)
def get_basket(current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")
    return basket
