from models import *
from models.bc import Bc
from models.house import House
from models.location import Location
from models.newbuilding import Newbuilding


class RivalOffer(Base):
    __tablename__ = 'rival_offers'
    id = Column(BigInteger, primary_key=True)
    cianUserId = Column(Integer)
    bc_id = Column(Integer, ForeignKey('bcs.id'))
    house_id = Column(Integer, ForeignKey('houses.id'))
    newbuilding_id = Column(Integer, ForeignKey('newbuildings.id'))

    description = Column(String)
    creationDate = Column(Date)
    editDate = Column(Date)
    publishDate = Column(Date)
    category = Column(Enum("office", "shoppingArea", "flat", "freeAppointmentObject", name='category', schema='cian'))
    dealType = Column(Enum("rent", "sale", name='dealType', schema='cian'))
    status = Column(Enum("published", name='status', schema='cian'))
    bargainTerms_currency = Column(Enum("rur", "usd", "eur", name='currency', schema='cian'))
    price = Column(BigInteger)
    pricePerUnitArea = Column(Integer)
    floorNumber = Column(SmallInteger)
    totalArea = Column(DECIMAL(7, 2))
    services = Column(Enum("top3", "paid", "premium", name='services', schema='cian'))
    userTrust = Column(Enum("involved", "notInvolved", "new", "excluded", name='userTrust', schema='cian'))
    isPro = Column(Boolean)
    stats_total = Column(SmallInteger)
    stats_daily = Column(SmallInteger)
    publishTerms_autoprolong = Column(Boolean)
    # Belongs to House
    house = relationship("House", back_populates="rivalOffers")
    newbuilding = relationship("Newbuilding")
    bc = relationship("Bc", back_populates="rivalOffers")
    # Have many Photos
    # photos = relationship("Photo", order_by=Photo.id, back_populates="offer")

    def __init__(self,
                 id,
                 cianUserId,
                 bc_id,
                 house_id,
                 newbuilding_id,
                 description,
                 creationDate,
                 editDate,
                 publishDate,
                 category,
                 dealType,
                 status,
                 bargainTerms_currency,
                 price,
                 pricePerUnitArea,
                 floorNumber,
                 totalArea,
                 services,
                 userTrust,
                 isPro,
                 stats_total,
                 stats_daily,
                 publishTerms_autoprolong):
        self.id = id
        self.cianUserId = cianUserId
        self.bc_id = bc_id
        self.house_id = house_id
        self.newbuilding_id = newbuilding_id
        self.description = description
        self.creationDate = creationDate
        self.editDate = editDate
        self.publishDate = publishDate
        self.category = category
        self.dealType = dealType
        self.status = status
        self.bargainTerms_currency = bargainTerms_currency
        self.price = price
        self.pricePerUnitArea = pricePerUnitArea
        self.floorNumber = floorNumber
        self.totalArea = totalArea
        self.services = services
        self.userTrust = userTrust
        self.isPro = isPro
        self.stats_total = stats_total
        self.stats_daily = stats_daily
        self.publishTerms_autoprolong = publishTerms_autoprolong
