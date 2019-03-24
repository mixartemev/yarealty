from sqlalchemy import create_engine, Column, ForeignKey, \
    Integer, BigInteger, SmallInteger, DECIMAL, String, Boolean, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create connection
engine = create_engine('postgresql://mix:321@localhost/yrlp', echo=False)
# Load Base class for declarative way tables operating
Base = declarative_base()


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, Sequence('photo_id_seq'), primary_key=True)
    offerId = Column(BigInteger, ForeignKey('offers.id'), nullable=True)
    # Belongs to Offer
    offer = relationship("Offer", back_populates="photos")
    url = Column(String)

    # Auto ?
    def __init__(self, offerId, url):
        # self.id = id
        self.offerId = offerId
        self.url = url

    def __repr__(self):
        return "<Photo('%s','%s', '%s')>" % (self.id, self.offerId, self.url)


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(BigInteger, primary_key=True)
    active = Column(Boolean)
    area = Column(DECIMAL(6, 2))
    buildingId = Column(Integer, ForeignKey('buildings.id'), nullable=True)
    # Belongs to Building
    building = relationship("Building", back_populates="offers")
    # Have many Photos
    photos = relationship("Photo", order_by=Photo.id, back_populates="offer")

    def __init__(self, id, active, area, buildingId):
        self.id = id
        self.active = active
        self.area = area
        self.buildingId = buildingId

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.id, self.area, self.active)


class Building(Base):
    __tablename__ = 'buildings'
    id = Column(BigInteger, primary_key=True)
    builtYear = Column(SmallInteger)
    builtQuarter = Column(SmallInteger)
    siteId = Column(Integer, nullable=True)
    # Have many Offers
    offers = relationship("Offer", order_by=Offer.id, back_populates="building")

    def __init__(self, id, builtYear, builtQuarter, siteId):
        self.id = id
        self.builtYear = builtYear
        self.builtQuarter = builtQuarter
        self.siteId = siteId

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.id, self.builtYear, self.siteId)


# Create all not created defined tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
