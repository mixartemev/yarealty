from sqlalchemy import func
from models import *


class HistoryPromo(Base):
    __tablename__ = 'history_promo'
    id = Column(Integer, ForeignKey('offers.id'), primary_key=True)
    date = Column(Date, primary_key=True, default=func.now())
    services = Column(Enum("top3", "premium", "paid", 'free', name='services', schema='cian'))
    offer = relationship("Offer", back_populates="promos")

    def __init__(self, id, services):
        self.id = id
        self.services = services
