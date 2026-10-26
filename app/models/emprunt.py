from datetime import date

from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
 
from database import Base

class Emprunt(Base):
    __tablename__ = "emprunt"
 
    id_emprunt = Column(Integer, primary_key=True, autoincrement=True)
    date_emprunt = Column(Date, nullable=False, default=date.today)
    date_retour_prevue = Column(Date, nullable=False)
    id_adherent = Column(Integer, ForeignKey("adherent.id_adherent"), nullable=False)
    id_ouvrage = Column(Integer, ForeignKey("ouvrage.id_ouvrage"), nullable=False)
 
    # Un emprunt concerne un adhérent et un ouvrage
    adherent = relationship("Adherent", back_populates="emprunts")
    ouvrage = relationship("Ouvrage", back_populates="emprunts")