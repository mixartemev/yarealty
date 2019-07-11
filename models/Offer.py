from datetime import datetime
from typing import List

from sqlalchemy import DateTime, func

from models import *
from models.bc import Bc
from models.historyPrice import HistoryPrice
from models.historyPromo import HistoryPromo
from models.house import House
from models.location import Location
from models.newbuilding import Newbuilding
from models.statsDaily import StatsDaily
from models.user import User


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    cianUserId = Column(Integer, ForeignKey('users.id'))
    bc_id = Column(Integer, ForeignKey('bcs.id'))
    house_id = Column(Integer, ForeignKey('houses.id'))
    newbuilding_id = Column(Integer, ForeignKey('newbuildings.id'))

    description = Column(String(4095))
    creationDate = Column(Date)
    editDate = Column(Date)
    publishDate = Column(Date)
    category = Column(Enum("office", "shoppingArea", "flat", "freeAppointmentObject", "newBuildingFlat",
                           name='category', schema='cian'))
    dealType = Column(Enum("rent", "sale", name='dealType', schema='cian'))
    status = Column(Enum("published", "draft", name='status', schema='cian'))
    currency = Column(Enum("rur", "usd", "eur", name='currency', schema='cian'))
    paymentPeriod = Column(Enum("monthly", "annual", name='paymentPeriod', schema='cian'))
    floorNumber = Column(SmallInteger)
    totalArea = Column(DECIMAL(7, 2))
    userTrust = Column(Enum("involved", "notInvolved", "new", "excluded", name='userTrust', schema='cian'))
    isPro = Column(Boolean)
    publishTerms_autoprolong = Column(Boolean)
    # Belongs to House
    house = relationship("House", back_populates="offers")
    newbuilding = relationship("Newbuilding")
    bc = relationship("Bc", back_populates="offers")
    # Have many Photos
    # photos = relationship("Photo", order_by=Photo.id, back_populates="offer")
    prices: List[HistoryPrice] = relationship("HistoryPrice", order_by=HistoryPrice.time, back_populates="offer")
    stats: List[StatsDaily] = relationship("StatsDaily", order_by=StatsDaily.date, back_populates="offer")
    promos: List[HistoryPromo] = relationship("HistoryPromo", order_by=HistoryPromo.date, back_populates="offer")
    user: User = relationship("User", back_populates="offers")
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    priceType = Column(Enum('squareMeter', 'all', name='priceType', schema='cian'))
    minArea = Column(DECIMAL(7, 2))

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
                 currency,
                 paymentPeriod,
                 floorNumber,
                 totalArea,
                 userTrust,
                 isPro,
                 publishTerms_autoprolong,
                 priceType,
                 minArea
                 ):
        self.id = id
        self.cianUserId = cianUserId
        self.bc_id = bc_id
        self.house_id = house_id
        self.newbuilding_id = newbuilding_id
        self.description = description
        self.creationDate = datetime.strptime(creationDate, '%Y-%m-%dT%H:%M:%S.%f').date()
        self.editDate = datetime.fromisoformat(editDate).date()
        self.publishDate = datetime.fromisoformat(publishDate).date()
        self.category = category
        self.dealType = dealType
        self.status = status
        self.currency = currency
        self.paymentPeriod = paymentPeriod
        self.floorNumber = floorNumber
        self.totalArea = totalArea
        self.userTrust = userTrust
        self.isPro = isPro
        self.publishTerms_autoprolong = publishTerms_autoprolong
        self.priceType = priceType
        self.minArea = minArea
