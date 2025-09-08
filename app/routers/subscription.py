from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


# ---------------CREATED ALL SUBSCRIPTION ROUTES----------------#
@router.post("/", response_model=schemas.SubscriptionOut)
def create(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    return crud.subscription.create_subscription(db, subscription)


@router.get("/", response_model=List[schemas.SubscriptionOut])
def read_subscriptions(db: Session = Depends(get_db)):
    return crud.subscription.get_subscriptions(db)


@router.get("/{subscription_id}", response_model=schemas.SubscriptionOut)
def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = crud.subscription.get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail=f"The subscription id:{subscription_id} does not exist",
        )
    return subscription


@router.put("/{subscription_id}", response_model=schemas.SubscriptionOut)
def update_subscription(
    subscription_id: int,
    subscription_data: schemas.SubscriptionCreate,
    db: Session = Depends(get_db),
):
    subscription = crud.subscription.update_subscription(db, subscription_id, subscription_data)
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail=f"The subscription id:{subscription_id} does not exist",
        )
    return subscription


@router.delete("/{subscription_id}", status_code=200)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    delete = crud.subscription.get_subscription(db, subscription_id)
    if not delete:
        raise HTTPException(status_code=404, detail=f"subscription id:{subscription_id} does not exist")
    crud.subscription.delete_subscription(db, subscription_id)
    return {"message": f"Schedule with ID {subscription_id} deleted successfully"}
