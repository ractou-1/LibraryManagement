from sqlalchemy.orm import Session

from app.models import Emprunt


class EmpruntRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Emprunt).all()

    def get_by_id(self, id_emprunt: int):
        return self.db.query(Emprunt).filter(Emprunt.id_emprunt == id_emprunt).first()

    def get_by_adherent(self, id_adherent: int):
        return self.db.query(Emprunt).filter(Emprunt.id_adherent == id_adherent).all()

    def get_by_ouvrage(self, id_ouvrage: int):
        return self.db.query(Emprunt).filter(Emprunt.id_ouvrage == id_ouvrage).all()

    def get_en_cours_by_ouvrage(self, id_ouvrage: int):
        return (
            self.db.query(Emprunt)
            .filter(Emprunt.id_ouvrage == id_ouvrage, Emprunt.date_retour.is_(None))
            .all()
        )

    def create(self, emprunt: Emprunt):
        self.db.add(emprunt)
        self.db.commit()
        self.db.refresh(emprunt)
        return emprunt

    def delete(self, emprunt: Emprunt):
        self.db.delete(emprunt)
        self.db.commit()