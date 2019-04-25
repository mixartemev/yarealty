from sqlalchemy import func
from models import *


class StatsDaily(Base):
    __tablename__ = 'stats_daily'
    id = Column(Integer, ForeignKey('offers.id'), primary_key=True)
    date = Column(Date, primary_key=True, default=func.now())
    stats_total = Column(SmallInteger)
    stats_daily = Column(SmallInteger)
    offer = relationship("Offer", back_populates="stats")

    def __init__(self, id, stats_total, stats_daily):
        self.id = id
        self.stats_total = stats_total
        self.stats_daily = stats_daily
