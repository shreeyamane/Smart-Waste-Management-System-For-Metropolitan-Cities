from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime

from app.core.database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)

    bin_id = Column(Integer, ForeignKey("bins.id"))

    fill_level = Column(Float)

    temperature = Column(Float)

    humidity = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)