from sqlalchemy.orm import Session
 
from app.models import Auteur

class AuteurRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Auteur).all()

    def get_by_id(self, id_auteur: int):
        return self.db.query(Auteur).filter(Auteur.id_auteur == id_auteur)
    
    def create(self, auteur: Auteur):
        self.db.add(auteur)
        self.db.commit()
        self.db.refresh(auteur)
        return auteur
 
    def delete(self, auteur: Auteur):
        self.db.delete(auteur)
        self.db.commit()