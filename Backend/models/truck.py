from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from db import Base


class Truck(Base):

    __tablename__ = "trucks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    truck_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    capacity_kg = Column(
        Float,
        default=5000
    )

    current_latitude = Column(
        Float
    )

    current_longitude = Column(
        Float
    )

    status = Column(
        String(30),
        default="AVAILABLE"
    )

    current_load_kg = Column(
        Float,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class TruckLocation(Base):

    __tablename__ = "truck_locations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    truck_id = Column(
        String(50),
        nullable=False,
        index=True
    )

    latitude = Column(
        Float,
        nullable=False
    )

    longitude = Column(
        Float,
        nullable=False
    )

    speed = Column(
        Float,
        default=0
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )