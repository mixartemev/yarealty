from models import *
from models.house import House


class Newbuilding(Base):
    __tablename__ = 'newbuildings'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    region_id = Column(Integer, ForeignKey('locations.id'))
    address = Column(String)
    # Belongs to Region
    region = relationship(
        "Location",  # foreign model name
        back_populates="newbuildings"  # this property name in foreign model
    )
    # Have many Houses
    houses = relationship("House", order_by=House.id, back_populates="newbuilding")

    def __init__(self, id, name, region_id, address):
        self.id = id
        self.name = name
        self.region_id = region_id
        self.address = address
