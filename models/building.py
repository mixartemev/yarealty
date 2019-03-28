from models import *
from models.offer import Offer


class Building(Base):
    __tablename__ = 'buildings'
    id = Column(BigInteger, primary_key=True)
    builtYear = Column(SmallInteger)
    builtQuarter = Column(SmallInteger)
    buildingState = Column(Enum("UNFINISHED", "bar", name='buildingState'))
    buildingType = Column(Enum("MONOLIT", "PANEL", name='buildingType'))
    siteId = Column(Integer, nullable=True)
    # Have many Offers
    offers = relationship("Offer", order_by=Offer.id, back_populates="building")

    def __init__(self, id, built_year, built_quarter, site_id):
        self.id = id
        self.builtYear = built_year
        self.builtQuarter = built_quarter
        self.siteId = site_id
