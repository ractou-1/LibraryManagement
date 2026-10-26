from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Auteur, Ouvrage

# Même base que celle d'Alembic (lance le script depuis la racine du projet)
engine = create_engine("sqlite:///library.db")
db = sessionmaker(bind=engine)()

hugo = Auteur(nom="Hugo", prenom="Victor", date_naissance=date(1802, 2, 26))

livre1 = Ouvrage(titre="Les Misérables", isbn="9782070409228", annee_publication=1862, auteur=hugo)
livre2 = Ouvrage(titre="Notre-Dame de Paris", isbn="9782070411573", annee_publication=1831, auteur=hugo)
livre3 = Ouvrage(titre="Les Contemplations", isbn="9782070411580", annee_publication=1856, auteur=hugo)

db.add_all([hugo, livre1, livre2, livre3])
db.commit()
print("Données ajoutées")