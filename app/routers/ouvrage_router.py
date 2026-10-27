from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Ouvrage
from app.repositories.auteur_repository import AuteurRepository
from app.repositories.emprunt_repository import EmpruntRepository
from app.repositories.ouvrage_repository import OuvrageRepository
from app.schemas.ouvrages import OuvrageCreate

router = APIRouter(prefix="/books")

#Lister les ouvrages
@router.get("")
def list_books(db: Session = Depends(get_db)):
    repo = OuvrageRepository(db)
    return repo.get_all()

#Créer un ouvrage
@router.post("", status_code=201)
def create_book(book: OuvrageCreate, db: Session = Depends(get_db)):
    repo = OuvrageRepository(db)

    # Règle métier : l'auteur doit exister
    if AuteurRepository(db).get_by_id(book.id_auteur) is None:
        raise HTTPException(status_code=404, detail="Auteur introuvable")

    # L'ISBN doit être unique
    if repo.get_by_isbn(book.isbn) is not None:
        raise HTTPException(status_code=409, detail="Cet ISBN existe déjà")

    new_book = Ouvrage(
        titre=book.titre,
        isbn=book.isbn,
        annee_publication=book.annee_publication,
        genre=book.genre,
        id_auteur=book.id_auteur,
    )
    return repo.create(new_book)

#Consulter un ouvrage par l'id
@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    repo = OuvrageRepository(db)
    book = repo.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Ouvrage introuvable")
    return book

#Supprimer un ouvrage
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    repo = OuvrageRepository(db)
    book = repo.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Ouvrage introuvable")

    # On refuse si des emprunts existent pour cet ouvrage
    if len(EmpruntRepository(db).get_by_ouvrage(book_id)) > 0:
        raise HTTPException(status_code=409, detail="Cet ouvrage a des emprunts")

    repo.delete(book)
    return {"message": "Ouvrage supprimé"}