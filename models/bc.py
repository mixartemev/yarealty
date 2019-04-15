from datetime import datetime

from sqlalchemy.orm import backref

from models import *


class Bc(Base):
    __tablename__ = 'bcs'
    id = Column(Integer, primary_key=True)
    typ = Column(Enum("БЦ", "ТЦ", name="typ"))
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('bcs.id'))
    address = Column(String)
    editDate = Column(Date)
    offers = relationship("Offer", back_populates="bc")
    # children = relationship("Bc", back_populates="parent")
    # parent = relationship("Bc", remote_side=[id],  back_populates="children")
    children = relationship("Bc", backref=backref('parent', remote_side=[id]))

    def __init__(self, id: int, typ: str, name: str, parent_id, address: str, editDate: str):
        self.id = id
        self.typ = typ
        self.name = name
        self.parent_id = parent_id if parent_id else None
        self.address = address
        self.editDate = datetime.strptime(editDate, "%d.%m.%Y").date()
