from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime
)

from db import Base


class Route(Base):

    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)

    truck_id = Column(
        String(50),
        nullable=False
    )

    route_date = Column(Date)

    total_distance_km = Column(Float)

    estimated_duration_min = Column(Float)

    status = Column(
        String(30),
        default="PLANNED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class RouteStop(Base):

    __tablename__ = "route_stops"

    id = Column(Integer, primary_key=True)

    route_id = Column(Integer)

    bin_id = Column(String(50))

    sequence = Column(Integer)

    estimated_arrival = Column(DateTime)

    actual_arrival = Column(DateTime)

    collection_status = Column(
        String(30),
        default="PENDING"
    )