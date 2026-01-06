from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from models.model import User
from models.category import Category
from schemas.schema import UserCreate, UserUpdate, UserLogin
from bmi_utils import calculate_bmi

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.get("/get")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    bmi = calculate_bmi(user.weight, user.height)

    category = db.query(Category).filter(
        Category.bmi_start <= bmi,
        Category.bmi_end >= bmi
    ).first()

    new_user = User(
        name=user.name,
        age=user.age,
        weight=user.weight,
        height=user.height,
        email=user.email,
        password=user.password,
        gender=user.gender,
        bmi=bmi,
        category_id=category.category_id if category else None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "user_id": new_user.user_id,
        "name": new_user.name,
        "email": new_user.email,
        "category_id": new_user.category_id
    }

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.email == user.email,
        User.password == user.password
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "user_id": db_user.user_id,
        "name": db_user.name,
        "email": db_user.email,
        "category_id": db_user.category_id
    }


@router.put("/{id}")
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_id == id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.name = user.name
    existing_user.age = user.age
    existing_user.weight = user.weight
    existing_user.height = user.height
    existing_user.email = user.email
    existing_user.password = user.password
    existing_user.gender = user.gender

    db.commit()
    db.refresh(existing_user)
    return existing_user


@router.get("/{id}")
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    category_name = None
    if user.category_id:
        category = db.query(Category).filter(
            Category.category_id == user.category_id
        ).first()
        if category:
            category_name = category.category

    return {
        "user_id": user.user_id,
        "name": user.name,
        "age": user.age,
        "weight": user.weight,
        "height": user.height,
        "bmi": user.bmi,
        "category": category_name,
        "email": user.email,
        "gender": user.gender
    }


@router.delete("/delete/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
















