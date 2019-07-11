from datetime import datetime
from models import *


class User(Base):
    __tablename__ = 'users'
    acc_map = [
        "?",
        "realtor",
        "agency",
        "uk",
        "owner",
    ]
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    creation_date = Column(Date)
    is_profi = Column(Boolean)
    is_private_broker = Column(Boolean)
    is_moderation_passed = Column(Boolean)
    status = Column(Enum("published", "hidden", name='userStatus', schema='cian'))
    account_type = Column(Enum("realtor", "agency", "uk", "owner", name='accType', schema='cian'))
    phones = relationship("Phone", back_populates="user")
    offers = relationship("Offer", back_populates="user")

    def __init__(self, id, name, creation_date, is_profi, is_private_broker, is_moderation_passed, status, account_type, phones):
        if account_type > 4:
            print(name)
        self.id = id
        self.name = name
        self.creation_date = datetime.fromisoformat(creation_date).date()
        self.is_profi = is_profi
        self.is_private_broker = is_private_broker
        self.is_moderation_passed = is_moderation_passed
        self.status = status
        self.account_type = self.acc_map[account_type]
        # self.phones = phones
