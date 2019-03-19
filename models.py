from sqlalchemy import create_engine, Column, ForeignKey,\
    Integer, BigInteger, DECIMAL, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create connection
engine = create_engine('postgresql://mix:321@localhost/yrlp', echo=False)
# Load Base class for declarative way tables operating
Base = declarative_base()


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(BigInteger, primary_key=True)
    active = Column(Boolean)
    area = Column(DECIMAL(6, 2))
    houseId = Column(Integer, nullable=True)
    siteId = Column(Integer, nullable=True)

    def __init__(self, id, active, area, houseId, siteId):
        self.id = id
        self.active = active
        self.area = area
        self.houseId = houseId
        self.siteId = siteId

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.id, self.area, self.active)


# Create all not created defined tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
