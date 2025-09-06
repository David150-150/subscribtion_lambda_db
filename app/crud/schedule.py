from sqlalchemy.orm import Session
from app.models import Schedule
from typing import List, Optional
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate 


#-----------------CREATE SCHEDULE------------#
def create_schedule(db: Session, schedule: ScheduleCreate) -> Schedule:
    new_schedule = Schedule(**schedule.dict())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

#-----------------GET ALL SCHEDULE------------#
def get_schedules(db: Session) -> List[Schedule]:
    return db.query(Schedule).all()

#-----------------GET SCHEDULE------------#
def get_schedule(db: Session, schedule_id: int) -> Optional[Schedule]:
    return db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()


#-----------------UPDATE SCHEDULE------------#
def update_schedule(db: Session, schedule_id: int, schedule_data: ScheduleUpdate) -> Optional[Schedule]:
    schedule = get_schedule(db, schedule_id)
    if not schedule:
        return None
    
    for key,value in schedule_data.dict(exclude_unset=True).items():
        setattr(schedule, key, value)


    db.commit()
    db.refresh(schedule)
    return schedule

#-----------------DELETE SCHEDULE------------#
def delete_schedule(db: Session, schedule_id: int) -> Optional[Schedule]:
    schedule = get_schedule(db, schedule_id)
    if not schedule:
        return None
    db.delete(schedule)
    db.commit()
    return schedule