from models import *


class Newbuilding(Base):
    __tablename__ = 'newbuildings'
    id = Column(BigInteger, primary_key=True)
    fkid = Column(Integer)
    name = Column(String)
    region = Column(String)  # , ForeignKey('buildings.id')
    address = Column(String)

    def __init__(self, id, fkid, name, region, address):
        self.id = id
        self.fkid = fkid
        self.name = name
        self.region = region
        self.address = address
