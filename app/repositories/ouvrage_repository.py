from sqlalchemy.orm import Session

from app.models import Ouvrage

class OuvrageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Ouvrage).all()

    def get_by_id(self, id_ouvrage: int):
        return self.db.query(Ouvrage).filter(Ouvrage.id_ouvrage == id_ouvrage).first()

    def get_by_isbn(self, isbn: str):
        return self.db.query(Ouvrage).filter(Ouvrage.isbn == isbn).first()

    def get_by_auteur(self, id_auteur: int):
        return self.db.query(Ouvrage).filter(Ouvrage.id_auteur == id_auteur).all()

    def search_by_titre(self, texte: str):
        return self.db.query(Ouvrage).filter(Ouvrage.titre.contains(texte)).all()

    def create(self, ouvrage: Ouvrage):
        self.db.add(ouvrage)
        self.db.commit()
        self.db.refresh(ouvrage)
        return ouvrage

    def delete(self, ouvrage: Ouvrage):
        self.db.delete(ouvrage)
        self.db.commit()