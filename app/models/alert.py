from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.core.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    bin_id = Column(Integer, ForeignKey("bins.id"))

    alert_type = Column(String)

    message = Column(String)

    status = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)