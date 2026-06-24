from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from app.core.database import Base


class BinReading(Base):
    __tablename__ = "bin_readings"

    id = Column(Integer, primary_key=True, index=True)

    bin_id = Column(String)

    fill_level = Column(Integer)

    weight = Column(Float)

    battery = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)