from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from db import get_db
from models.alert import Alert


router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"]
)


def model_to_dict(obj):

    mapper = inspect(obj).mapper

    return {
        column.key: getattr(obj, column.key)
        for column in mapper.column_attrs
    }


@router.get("/")
def get_alerts(
    db: Session = Depends(get_db)
):

    alerts = (
        db.query(Alert)
        .all()
    )

    return [
        model_to_dict(alert)
        for alert in alerts
    ]