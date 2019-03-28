from models import *
from models.photo import Photo


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(BigInteger, primary_key=True)
    active = Column(Boolean)
    area = Column(DECIMAL(6, 2))
    buildingId = Column(BigInteger, ForeignKey('buildings.buildingId'), nullable=True)
    # Belongs to Building
    building = relationship("Building", back_populates="offers")
    # Have many Photos
    photos = relationship("Photo", order_by=Photo.id, back_populates="offer")

    def __init__(self, id, active, area, building_id):
        self.id = id
        self.active = active
        self.area = area
        self.buildingId = building_id
