from models import *
from models.building import Building


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    displayName = Column(String)
    # Have many Buildings
    buildings = relationship("Building", order_by=Building.id, back_populates="site")

    def __init__(self, id, name, displayName):
        self.id = id
        self.name = name
        self.displayName = displayName
