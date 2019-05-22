from models import *
from models.phone import Phone


class User(Base):
    __tablename__ = 'users'
    acc_map = [
        "?"
        "realtor",
        "agency",
        "uk",
        "owner",
    ]
    id = Column(Integer, primary_key=True)
    name = Column(String)
    creation_date = Column(Date)
    is_profi = Column(Boolean)
    is_private_broker = Column(Boolean)
    is_moderation_passed = Column(Boolean)
    status = Column(Enum("published", "hidden", name='userStatus', schema='cian'))
    account_type = Column(Enum("realtor", "agency", "uk", "owner", name='accType', schema='cian'))
    phones = relationship("Phone", back_populates="user")

    def __init__(self, id, name, creation_date, is_profi, is_private_broker, is_moderation_passed, status, account_type, phones):
        self.id = id
        self.name = name
        self.creation_date = creation_date
        self.is_profi = is_profi
        self.is_private_broker = is_private_broker
        self.is_moderation_passed = is_moderation_passed
        self.status = status
        self.account_type = account_type
        self.phones = phones
