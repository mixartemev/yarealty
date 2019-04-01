from models import *
from models.offer import Offer


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    partnerInternalId = Column(BigInteger)
    partnerName = Column(String)
    agentName = Column(String)
    category = Column(String)
    encryptedPhone = Column(String)
    redirectId = Column(String, nullable=True)
    # Have many Offers
    offers = relationship("Offer", order_by=Offer.id, back_populates="author")

    def __init__(self, id, partnerInternalId, partnerName, agentName, category, encryptedPhone, redirectId):
        self.id = id
        self.partnerInternalId = partnerInternalId
        self.partnerName = partnerName
        self.agentName = agentName
        self.category = category
        self.encryptedPhone = encryptedPhone
        self.redirectId = redirectId
