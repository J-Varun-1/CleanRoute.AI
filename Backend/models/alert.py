from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)

from db import Base



class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    bin_id = Column(String(50))

    severity = Column(String(30))

    message = Column(String(255))

    is_resolved = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )