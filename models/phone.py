from models import *


class Phone(Base):
    __tablename__ = 'phones'
    user_id = Column(Integer, primary_key=True)
    phone = Column(String, primary_key=True)
    user = relationship("User", back_populates="phones")

    def __init__(self, user_id, phone):
        self.user_id = user_id
        self.phone = phone
