from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from db import Base


class Collection(Base):

    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)

    bin_id = Column(String(50))

    truck_id = Column(String(50))

    route_id = Column(Integer)

    collected_amount_kg = Column(Float)

    wet_amount_kg = Column(Float)

    dry_amount_kg = Column(Float)

    collected_at = Column(
        DateTime,
        default=datetime.utcnow
    )