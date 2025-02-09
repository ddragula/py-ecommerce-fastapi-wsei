from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
from ..database import SessionLocal
from ..models import Order, OrderItem, Basket, BasketItem, Product, User
from ..services import SECRET_KEY, ALGORITHM, order_to_xml
from ..schemas import Order as OrderSchema

router = APIRouter(
    prefix="/api/orders",
    tags=["orders"]
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


@router.post("/place", response_model=OrderSchema)
def place_order(current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not basket or not basket.items:
        raise HTTPException(status_code=400, detail="Basket is empty")
    # Create order
    order = Order(user_id=current_user.id)
    db.add(order)
    db.commit()
    db.refresh(order)

    for basket_item in basket.items:
        product = db.query(Product).filter(Product.id == basket_item.product_id).first()
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=basket_item.quantity,
            price=product.price
        )
        db.add(order_item)
    # Clear basket
    db.query(BasketItem).filter(BasketItem.basket_id == basket.id).delete()
    db.commit()
    db.refresh(order)
    return order


@router.get("/", response_model=List[OrderSchema])
def get_orders(current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


@router.get("/{order_id}/xml")
def get_order_xml(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    xml_data = order_to_xml(order)
    return Response(content=xml_data, media_type="application/xml")
