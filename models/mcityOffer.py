from sqlalchemy import DateTime, func

from models import *
from models.bc import Bc
from models.house import House
from models.location import Location
from models.newbuilding import Newbuilding


class McityOffer(Base):
    __tablename__ = 'mcity_offers'
    id = Column(BigInteger, primary_key=True)
    idd = Column(Integer)
    bc_id = Column(Integer, ForeignKey('bcs.id'))
    house_id = Column(Integer, ForeignKey('houses.id'))
    newbuilding_id = Column(Integer, ForeignKey('newbuildings.id'))

    description = Column(String)
    creationDate = Column(Date)
    editDate = Column(Date)
    publishDate = Column(Date)
    # offerType = Column(Enum("commercial", "flat", name='offerType'))
    category = Column(Enum("office", "shoppingArea", "flat", "freeAppointmentObject", "newBuildingFlat",
                           name='category', schema='cian'))
    dealType = Column(Enum("rent", "sale", name='dealType', schema='cian'))
    status = Column(Enum("published", name='status', schema='cian'))
    currency = Column(Enum("rur", "usd", "eur", name='currency', schema='cian'))
    paymentPeriod = Column(Enum("monthly", "annual", name='paymentPeriod', schema='cian'))
    floorNumber = Column(SmallInteger)
    totalArea = Column(DECIMAL(6, 2))
    userTrust = Column(Enum("involved", "notInvolved", "new", "excluded", name='userTrust', schema='cian'))
    isPro = Column(Boolean)

    publishTerms_autoprolong = Column(Boolean)
    # Belongs to House
    house = relationship("House", back_populates="mcityOffers")
    newbuilding = relationship("Newbuilding")
    bc = relationship("Bc", back_populates="mcityOffers")
    # Have many Photos
    # photos = relationship("Photo", order_by=Photo.id, back_populates="offer")
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())

    def __init__(self,
                 id,
                 idd,
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
                 publishTerms_autoprolong):
        self.id = id
        self.idd = idd
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
        self.currency = currency
        self.paymentPeriod = paymentPeriod
        self.floorNumber = floorNumber
        self.totalArea = totalArea
        self.userTrust = userTrust
        self.isPro = isPro
        self.publishTerms_autoprolong = publishTerms_autoprolong
