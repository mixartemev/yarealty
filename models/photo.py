from models import *


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, Sequence('photo_id_seq'), primary_key=True)
    offerId = Column(BigInteger, ForeignKey('offers.id'), nullable=True)
    # Belongs to Offer
    offer = relationship("Offer", back_populates="photos")
    url = Column(String)

    def __init__(self, offer_id, url):
        # self.id = id
        self.offerId = offer_id
        self.url = url
