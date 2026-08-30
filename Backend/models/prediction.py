from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey
)

from db import Base


class BinPrediction(Base):

    __tablename__ = "bin_predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    bin_id = Column(
        String(50),
        ForeignKey("bins.bin_id"),
        nullable=False,
        index=True
    )

    prediction_date = Column(
        Date,
        nullable=False,
        index=True
    )

    fill_percentage = Column(Float)

    wet_waste_pct = Column(Float)

    dry_waste_pct = Column(Float)

    predicted_waste_kg = Column(Float)

    model_version = Column(
        String(50)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )