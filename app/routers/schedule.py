from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


# ------------CREATED ALL SCHEDULE ROUTES--------------#
@router.post("/", response_model=schemas.ScheduleOut)
def create_schema(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    return crud.schedule.create_schedule(db, schedule)


@router.get("/", response_model=List[schemas.ScheduleOut])
def read_schedules(db: Session = Depends(get_db)):
    return crud.schedule.get_schedules(db)


@router.get("/{schedule_id}", response_model=schemas.ScheduleOut)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = crud.schedule.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail=f"The ID:{schedule_id}, does not exist")
    return schedule


@router.put("/{schedule_id}", response_model=schemas.ScheduleOut)
def update_schedule(
    schedule_id: int,
    schedule_data: schemas.ScheduleUpdate,
    db: Session = Depends(get_db),
):
    schedule = crud.schedule.update_schedule(db, schedule_id, schedule_data)
    if not schedule:
        raise HTTPException(status_code=404, detail=f"The ID:{schedule_id}, does not exist")
    return schedule


@router.delete("/{schedule_id}", status_code=200)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = crud.schedule.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail=f"The ID:{schedule_id}, does not exist")
    crud.schedule.delete_schedule(db, schedule_id)
    return {"message": f"Schedule with ID {schedule_id} deleted successfully"}
