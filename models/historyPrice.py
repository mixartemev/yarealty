from datetime import datetime
from models import *


class HistoryPrice(Base):
    __tablename__ = 'history_price'
    id = Column(Integer, ForeignKey('offers.id'), primary_key=True)
    time = Column(DateTime, primary_key=True)
    price = Column(BigInteger)
    offer = relationship("Offer", back_populates="prices")

    def __init__(self, id, time, price):
        self.id = id
        self.time = datetime.utcfromtimestamp(time)
        self.price = price
