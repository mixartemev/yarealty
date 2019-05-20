from models import *


class Match(Base):
    __tablename__ = 'matches'
    idd = Column(Integer, primary_key=True)
    id = Column(BigInteger, primary_key=True)

    def __init__(self, id, idd):
        self.id = id
        self.idd = idd
