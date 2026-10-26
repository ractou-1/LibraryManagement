from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
 
from app.database import Base
 
 
class Auteur(Base):
    __tablename__ = "auteur"
 
    id_auteur = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_naissance = Column(Date, nullable=True)
 
    # Un auteur a plusieurs ouvrages
    ouvrages = relationship("Ouvrage", back_populates="auteur")