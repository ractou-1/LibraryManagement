from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Auteur
from app.repositories.auteur_repository import AuteurRepository
from app.repositories.ouvrage_repository import OuvrageRepository
from app.schemas.auteurs import AuteurCreate

router = APIRouter(prefix="/authors")

#Lister les auteurs
@router.get("")
def list_authors(db: Session = Depends(get_db)):
    repo = AuteurRepository(db)
    return repo.get_all()

#Créer un auteur
@router.post("", status_code=201)
def create_author(author: AuteurCreate, db: Session = Depends(get_db)):
    repo = AuteurRepository(db)
    new_author = Auteur(
        nom=author.nom,
        prenom=author.prenom,
        date_naissance=author.date_naissance,
    )
    return repo.create(new_author)

#Consulter un auteur
@router.get("/{author_id}")
def get_author(author_id: int, db: Session = Depends(get_db)):
    repo = AuteurRepository(db)
    author = repo.get_by_id(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Auteur introuvable")
    return author

#Rechercher les ouvrages d'un auteur
@router.get("/{author_id}/books")
def list_author_books(author_id: int, db: Session = Depends(get_db)):
    author = AuteurRepository(db).get_by_id(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Auteur introuvable")
    return OuvrageRepository(db).get_by_auteur(author_id)