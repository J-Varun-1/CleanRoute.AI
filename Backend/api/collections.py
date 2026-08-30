from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from db import get_db
from models.collection import Collection


router = APIRouter(
    prefix="/api/collections",
    tags=["Collections"]
)


def model_to_dict(obj):

    mapper = inspect(obj).mapper

    return {
        column.key: getattr(obj, column.key)
        for column in mapper.column_attrs
    }


@router.get("/")
def get_collections(
    db: Session = Depends(get_db)
):

    collections = (
        db.query(Collection)
        .all()
    )

    return [
        model_to_dict(collection)
        for collection in collections
    ]