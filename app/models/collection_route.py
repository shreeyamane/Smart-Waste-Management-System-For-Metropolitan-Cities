from sqlalchemy import Column, Integer, String

from app.core.database import Base

class CollectionRoute(Base):
    __tablename__ = "collection_routes"

    id = Column(Integer, primary_key=True)

    vehicle_number = Column(String)

    driver_name = Column(String)

    assigned_bins = Column(String)

    route_status = Column(String)