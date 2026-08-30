from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from db import Base


class Bin(Base):

    __tablename__ = "bins"

    id = Column(Integer, primary_key=True, index=True)

    bin_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    area_type = Column(String(50))

    population_density = Column(Float)

    capacity_kg = Column(Float, default=1000)

    status = Column(
        String(30),
        default="NORMAL"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )