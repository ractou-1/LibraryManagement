from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Emprunt
from app.repositories.adherent_repository import AdherentRepository
from app.repositories.emprunt_repository import EmpruntRepository
from app.repositories.ouvrage_repository import OuvrageRepository
from app.schemas.emprunts import EmpruntCreate

router = APIRouter(prefix="/loans")

#Consulter les emprunts
@router.get("")
def list_loans(db: Session = Depends(get_db)):
    repo = EmpruntRepository(db)
    return repo.get_all()

# Les emprunts en cours = ceux qui n'ont pas de date de retour
@router.get("/ongoing")
def list_encours_loans(db: Session = Depends(get_db)):
    repo = EmpruntRepository(db)
    return repo.get_en_cours()

#Créer un emprunt
@router.post("", status_code=201)
def create_loan(loan: EmpruntCreate, db: Session = Depends(get_db)):
    # Les dates sont déjà vérifiées par le schéma EmpruntCreate

    # Règle métier : l'adhérent et l'ouvrage doivent exister
    if AdherentRepository(db).get_by_id(loan.id_adherent) is None:
        raise HTTPException(status_code=404, detail="Adhérent introuvable")
    if OuvrageRepository(db).get_by_id(loan.id_ouvrage) is None:
        raise HTTPException(status_code=404, detail="Ouvrage introuvable")

    repo = EmpruntRepository(db)

    # Règle métier : l'ouvrage ne doit pas déjà être emprunté
    if len(repo.get_en_cours_by_ouvrage(loan.id_ouvrage)) > 0:
        raise HTTPException(status_code=409, detail="Cet ouvrage est déjà emprunté")

    new_loan = Emprunt(
        id_adherent=loan.id_adherent,
        id_ouvrage=loan.id_ouvrage,
        duree=loan.duree,
        date_emprunt=loan.date_emprunt,
        date_retour=loan.date_retour,
    )
    return repo.create(new_loan)


# Enregistre le retour d'un ouvrage : la date de retour devient la date du jour
@router.put("/{loan_id}/return")
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    repo = EmpruntRepository(db)
    loan = repo.get_by_id(loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Emprunt introuvable")
    if loan.date_retour is not None:
        raise HTTPException(status_code=409, detail="Cet emprunt est déjà rendu")

    # Règle métier : le retour ne peut pas être avant le début de l'emprunt
    if date.today() < loan.date_emprunt:
        raise HTTPException(
            status_code=400,
            detail="La date de retour ne peut pas être antérieure à la date d'emprunt",
        )

    loan.date_retour = date.today()
    return repo.update(loan)