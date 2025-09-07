from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate


# -----------------CREATE SUBSCRIPTION------------#
def create_subscription(db: Session, subscription: SubscriptionCreate) -> Subscription:
    new_subscription = Subscription(**subscription.dict())
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription


# -----------------GET ALL SUBSCRIPTION------------#
def get_subscriptions(db: Session) -> List[Subscription]:
    return db.query(Subscription).all()


# -----------------GET SUBSCRIPTION------------#
def get_subscription(db: Session, subscription_id: int) -> Optional[Subscription]:
    return (
        db.query(Subscription)
        .filter(Subscription.subscription_id == subscription_id)
        .first()
    )


# -----------------UPDATE SUBSCRIPTION------------#
def update_subscription(
    db: Session, subscription_id: int, subscription_data: SubscriptionUpdate
) -> Optional[Subscription]:
    subscription = get_subscription(db, subscription_id)
    if not subscription:
        return None

    for key, value in subscription_data.dict(exclude_unset=True).items():
        setattr(subscription, key, value)

    db.commit()
    db.refresh(subscription)
    return subscription


# -----------------DELETE SUBSCRIPTION------------#
def delete_subscription(db: Session, subscription_id: int) -> Optional[Subscription]:
    subscription = get_subscription(db, subscription_id)
    if not subscription:
        return None
    db.delete(subscription)
    db.commit()
    return subscription
