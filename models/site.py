from models import *


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Site('%s','ЖК «%s»')>" % (self.id, self.name)
