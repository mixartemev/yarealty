from models import *
from models.offer import Offer


class Building(Base):
    __tablename__ = 'buildings'
    id = Column(BigInteger, primary_key=True)
    builtYear = Column(SmallInteger)
    buildingType = Column(Enum("MONOLIT", "PANEL", "BRICK", "MONOLIT_BRICK", "BLOCK", "WOOD", name='buildingType'))
    floorsTotal = Column(SmallInteger)

    # Have many Offers
    offers = relationship("Offer", order_by=Offer.id, back_populates="building")

    def __init__(self, id, built_year, building_type, floors_total):
        self.id = id
        self.builtYear = built_year
        self.buildingType = building_type
        self.floorsTotal = floors_total
