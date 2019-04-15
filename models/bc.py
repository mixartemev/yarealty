from models import *


class Bc(Base):
    __tablename__ = 'bcs'
    id = Column(Integer, primary_key=True)
    typ = Column(Enum("БЦ", "ТЦ", name="typ"))
    name = Column(String)
    parent_id = Column(Integer)
    address = Column(String)
    editDate = Column(Date)
    offers = relationship("Offer", back_populates="bc")

    def __init__(self, id, typ, name, parent_id, address, editDate):
        self.id = id
        self.typ = typ
        self.name = name
        self.parent_id = parent_id if parent_id else None
        self.address = address
        self.editDate = editDate
