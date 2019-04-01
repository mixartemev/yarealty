from models import *
from models.offer import Offer


class Building(Base):
    __tablename__ = 'buildings'
    id = Column(BigInteger, Sequence('building_id_seq'), primary_key=True, autoincrement=True)
    buildingId = Column(BigInteger, nullable=True, index=True, unique=True)
    builtYear = Column(SmallInteger)
    builtQuarter = Column(SmallInteger)
    buildingState = Column(Enum("UNFINISHED", "HAND_OVER", name='buildingState'))
    buildingType = Column(Enum("MONOLIT", "PANEL", "BRICK", "MONOLIT_BRICK", "BLOCK", "WOOD", name='buildingType'))
    siteId = Column(Integer, ForeignKey('sites.id'), nullable=True)
    houseId = Column(Integer, nullable=True)
    floorsTotal = Column(SmallInteger)

    # Belongs to Site
    site = relationship("Site", back_populates="buildings")
    # Have many Offers
    offers = relationship("Offer", order_by=Offer.id, back_populates="building")

    def __init__(self, building_id, built_year, built_quarter, building_state, building_type, site_id, house_id,
                 floors_total):
        # self.id = id
        self.buildingId = building_id
        self.builtYear = built_year
        self.builtQuarter = built_quarter
        self.buildingState = building_state
        self.buildingType = building_type
        self.siteId = site_id
        self.houseId = house_id
        self.floorsTotal = floors_total
