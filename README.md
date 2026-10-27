# Gestion d'une médiathèque

API web (FastAPI + SQLAlchemy) pour gérer les auteurs, ouvrages, adhérents et emprunts d'une médiathèque.

Toutes les commandes se lancent depuis la **racine du projet**.

## Installation

```
pip install fastapi uvicorn sqlalchemy alembic
```

## Créer la base de données

La base (`library.db`, SQLite) est créée par les migrations Alembic :

```
python -m alembic upgrade head
```

Cette commande reconstruit entièrement le schéma sur une base vide, en appliquant les migrations dans l'ordre.

## Charger les données de test (fixtures)

Une fois la base créée :

```
python fixtures.py
```

Le script affiche `Fixtures chargées avec succès.`

Les données sont variées pour pouvoir tester les différentes fonctionnalités :

- des ouvrages avec un genre et d'autres sans genre (`NULL`) ;
- un auteur avec trois ouvrages, d'autres avec un ou deux ;
- un adhérent avec plusieurs emprunts, un autre sans aucun emprunt ;
- 4 emprunts en cours (sans date de retour), dont un en retard, et 3 emprunts rendus ;
- des durées de prêt différentes (7, 14 et 21 jours) ;
- un même ouvrage emprunté plusieurs fois à des dates différentes.

## Repartir de zéro

Pour supprimer la base et la reconstruire avec les données de test :

```
del library.db
python -m alembic upgrade head
python fixtures.py
```

## Lancer l'application

```
uvicorn main:app --reload
```

La documentation l'API est disponible sur http://127.0.0.1:8000/docs.
