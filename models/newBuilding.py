from models import *
from models.offer import Offer


class NewBuilding(Base):
    __tablename__ = 'new_buildings'
    id = Column(BigInteger, Sequence('new_building_id_seq'), primary_key=True, autoincrement=True)
    builtYear = Column(SmallInteger)
    builtQuarter = Column(SmallInteger)
    buildingState = Column(Enum("UNFINISHED", "HAND_OVER", name='buildingState'))
    buildingType = Column(Enum("MONOLIT", "PANEL", "BRICK", "MONOLIT_BRICK", "BLOCK", "WOOD", name='buildingType'))
    siteId = Column(Integer, ForeignKey('sites.id'), nullable=True)
    houseId = Column(Integer, nullable=True)
    floorsTotal = Column(SmallInteger)

    # Belongs to Site
    site = relationship("Site", back_populates="newBuildings")
    # Have many Offers
    offers = relationship("Offer", order_by=Offer.id, back_populates="newBuilding")

    def __init__(self, built_year, built_quarter, building_state, building_type, site_id, house_id, floors_total):
        self.builtYear = built_year
        self.builtQuarter = built_quarter
        self.buildingState = building_state
        self.buildingType = building_type
        self.siteId = site_id
        self.houseId = house_id
        self.floorsTotal = floors_total
