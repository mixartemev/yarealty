from models import *


class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    newbuilding_id = Column(Integer)  # , ForeignKey('buildings.id')
    name = Column(String)
    address = Column(String)

    def __init__(self, id, newbuilding_id, name, address):
        self.id = id
        self.newbuilding_id = newbuilding_id
        self.name = name
        self.address = address
