from models import *
from models.photo import Photo


class Offer(Base):
    __tablename__ = 'offers'
    buildingId = Column(BigInteger, ForeignKey('buildings.id'))
    newBuildingId = Column(BigInteger, ForeignKey('new_buildings.id'))
    id = Column(BigInteger, primary_key=True)
    trust = Column(String)
    active = Column(Boolean)
    rooms = Column(SmallInteger)
    price = Column(Integer)
    price_m2 = Column(Integer)
    floor = Column(SmallInteger)
    area = Column(DECIMAL(6, 2))
    livingSpace = Column(DECIMAL(6, 2))
    roomSpace = Column(ARRAY(DECIMAL(5, 2)))
    kitchenSpace = Column(DECIMAL(6, 2))
    partnerId = Column(Integer, ForeignKey('author.id'))
    creationDate = Column(Date)
    description = Column(String)
    # Belongs to Building
    building = relationship("Building", back_populates="offers")
    newBuilding = relationship("NewBuilding", back_populates="offers")
    author = relationship("Author", back_populates="offers")
    # Have many Photos
    photos = relationship("Photo", order_by=Photo.id, back_populates="offer")

    def __init__(self, new_building_id, building_id, id, trust, active, rooms, price, price_m2, floor, area, living_space, room_space,
                 kitchen_space, partner_id, creation_date, description):
        self.newBuildingId = new_building_id
        self.buildingId = building_id
        self.id = id
        self.trust = trust
        self.active = active
        self.rooms = rooms
        self.price = price
        self.price_m2 = price_m2
        self.floor = floor
        self.area = area
        self.livingSpace = living_space
        self.roomSpace = room_space
        self.kitchenSpace = kitchen_space
        self.partnerId = partner_id
        self.creationDate = creation_date
        self.description = description
