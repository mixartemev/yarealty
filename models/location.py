from models import *
from models.newbuilding import Newbuilding


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Have many Newbuildings
    newbuildings = relationship("Newbuilding", order_by=Newbuilding.id, back_populates="region")

    def __init__(self, id, name):
        self.id = id
        self.name = name
