from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
 
from database import Base

class Adherent(Base):
    __tablename__ = "adherent"
 
    id_adherent = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
 
    # Un adhérent peut faire plusieurs emprunts
    emprunts = relationship("Emprunt", back_populates="adherent")