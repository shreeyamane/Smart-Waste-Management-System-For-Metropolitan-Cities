from sqlalchemy import Column, Integer, String, Float

from app.core.database import Base


class Bin(Base):
    __tablename__ = "bins"

    id = Column(Integer, primary_key=True, index=True)

    bin_code = Column(String, unique=True)

    location = Column(String)

    latitude = Column(Float)

    longitude = Column(Float)

    status = Column(String)

    fill_level = Column(Integer)

    weight = Column(Float)

    battery = Column(Integer)