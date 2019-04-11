from models import *


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(BigInteger, primary_key=True)
    businessShoppingCenter_id = Column(Integer)  # , ForeignKey('buildings.id')
    newbuilding_id = Column(Integer)  # , ForeignKey('new_buildings.id')
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

    def __init__(self,
                 id,
                 businessShoppingCenter_id,
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
        self.businessShoppingCenter_id = businessShoppingCenter_id
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
