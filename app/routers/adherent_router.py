from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Adherent
from app.repositories.adherent_repository import AdherentRepository
from app.repositories.emprunt_repository import EmpruntRepository
from app.schemas.adherents import AdherentCreate

router = APIRouter(prefix="/members")

#Lister les adhérents
@router.get("")
def list_members(db: Session = Depends(get_db)):
    repo = AdherentRepository(db)
    return repo.get_all()

#Création d'un adhérent
@router.post("", status_code=201)
def create_member(member: AdherentCreate, db: Session = Depends(get_db)):
    repo = AdherentRepository(db)

    # L'email doit être unique
    if repo.get_by_email(member.email) is not None:
        raise HTTPException(status_code=409, detail="Cet email existe déjà")

    new_member = Adherent(
        nom=member.nom,
        prenom=member.prenom,
        email=member.email,
    )
    return repo.create(new_member)

#Consulter les emprunts d'un adhérent 
@router.get("/{member_id}/loans")
def list_member_loans(member_id: int, db: Session = Depends(get_db)):
    member = AdherentRepository(db).get_by_id(member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Adhérent introuvable")
    return EmpruntRepository(db).get_by_adherent(member_id)