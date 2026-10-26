from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
 
from database import Base

class Ouvrage(Base):
    __tablename__ = "ouvrage"
 
    id_ouvrage = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(200), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True)
    annee_publication = Column(Integer, nullable=False)
    genre = Column(String(50), nullable=True)
    id_auteur = Column(Integer, ForeignKey("auteur.id_auteur"), nullable=False)
 
    # Un ouvrage a un auteur et peut avoir plusieurs emprunts
    auteur = relationship("Auteur", back_populates="ouvrages")
    emprunts = relationship("Emprunt", back_populates="ouvrage")