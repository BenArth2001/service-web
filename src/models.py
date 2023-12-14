from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Trad(Base):
    __tablename__ = "trads"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(40))
    dictionnary = Column(String(40))
    trad = Column(String(40))

class Dictionnary(Base):
    __tablename__ = "dictionnaries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))

    lines = relationship("DictionnaryLine", back_populates="dictionnary")

class DictionnaryLine(Base):
    __tablename__ = "dictionnaries_lines"

    id = Column(Integer, primary_key=True, index=True)
    lineKey = Column(String(2))
    lineValue = Column(String(5))
    dictionnary_id = Column(Integer, ForeignKey("dictionnaries.id"))

    dictionnary = relationship("Dictionnary", back_populates="lines")