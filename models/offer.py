from models import *


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(BigInteger, primary_key=True)
    bc_id = Column(Integer, ForeignKey('bcs.id'))
    house_id = Column(Integer, ForeignKey('houses.id'))
    newbuilding_id = Column(Integer, ForeignKey('newbuildings.id'))

    description = Column(String)
    creationDate = Column(Date)
    editDate = Column(Date)
    publishDate = Column(Date)
    offerType = Column(Enum("commercial", "living", name='offerType'))
    dealType = Column(Enum("rent", "sell", name='dealType'))
    status = Column(Enum("published", name='status'))
    bargainTerms_currency = Column(Enum("rur", "usd", "eur", name='currency'))
    price = Column(Integer)
    pricePerUnitArea = Column(Integer)
    floorNumber = Column(SmallInteger)
    totalArea = Column(DECIMAL(6, 2))
    services = Column(Enum("top3", "paid", name='services'))
    userTrust = Column(Enum("involved", name='userTrust'))
    isPro = Column(Boolean)
    publishTerms_autoprolong = Column(Boolean)
    # Belongs to House
    house = relationship("House", back_populates="offers")
    newbuilding = relationship("Newbuilding")
    bc = relationship("Bc", back_populates="offers")
    # Have many Photos
    # photos = relationship("Photo", order_by=Photo.id, back_populates="offer")

    def __init__(self,
                 id,
                 bc_id,
                 house_id,
                 newbuilding_id,
                 description,
                 creationDate,
                 editDate,
                 publishDate,
                 offerType,
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
                 publishTerms_autoprolong):
        self.id = id
        self.bc_id = bc_id
        self.house_id = house_id
        self.newbuilding_id = newbuilding_id
        self.description = description
        self.creationDate = creationDate
        self.editDate = editDate
        self.publishDate = publishDate
        self.offerType = offerType
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
        self.publishTerms_autoprolong = publishTerms_autoprolong
