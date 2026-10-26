from sqlalchemy.orm import Session

from app.models import Adherent


class AdherentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Adherent).all()

    def get_by_id(self, id_adherent: int):
        return self.db.query(Adherent).filter(Adherent.id_adherent == id_adherent).first()

    def get_by_email(self, email: str):
        return self.db.query(Adherent).filter(Adherent.email == email).first()

    def create(self, adherent: Adherent):
        self.db.add(adherent)
        self.db.commit()
        self.db.refresh(adherent)
        return adherent

    def delete(self, adherent: Adherent):
        self.db.delete(adherent)
        self.db.commit()