from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from db import get_db
from models.truck import Truck


router = APIRouter(
    prefix="/api/trucks",
    tags=["Trucks"]
)


def model_to_dict(obj):

    mapper = inspect(obj).mapper

    return {
        column.key: getattr(obj, column.key)
        for column in mapper.column_attrs
    }


@router.get("/")
def get_all_trucks(
    db: Session = Depends(get_db)
):

    trucks = db.query(Truck).all()

    return [
        model_to_dict(truck)
        for truck in trucks
    ]


@router.get("/{truck_id}")
def get_truck(
    truck_id: int,
    db: Session = Depends(get_db)
):

    truck = (
        db.query(Truck)
        .filter(Truck.id == truck_id)
        .first()
    )

    if truck is None:

        raise HTTPException(
            status_code=404,
            detail="Truck not found"
        )

    return model_to_dict(truck)