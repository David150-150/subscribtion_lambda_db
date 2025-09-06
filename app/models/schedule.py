from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql import func
from app.db import Base


#--------------CREATE SCHEDULE TABLE------------#
class Schedule(Base):
    __tablename__ = "schedule"

    schedule_id = Column(Integer, primary_key = True, index = True)
    task_name = Column(String(50))
    subscription_id = Column(Integer, ForeignKey("subscription.subscription_id"), nullable = False)
    schedule_date = Column(Date, default=func.current_date(), nullable=False) 
    status = Column(Enum("pending", "complete", "cancelled", name = "schedule_status_name"), nullable = False, default = "pending")
    created_at = Column(TIMESTAMP, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = func.now(), onupdate = func.now())
