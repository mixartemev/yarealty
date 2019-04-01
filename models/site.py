from models import *
from models.newBuilding import NewBuilding


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    displayName = Column(String)
    # Have many Buildings
    newBuildings = relationship("NewBuilding", order_by=NewBuilding.id, back_populates="site")

    def __init__(self, id, name, display_name):
        self.id = id
        self.name = name
        self.displayName = display_name
