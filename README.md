# Gestion d'une médiathèque

API web (FastAPI + SQLAlchemy + Alembic) pour la gestion des auteurs, des ouvrages, des adhérents et des emprunts d'une médiathèque.

## Prérequis

- Python 3.10 ou plus récent
- pip

Aucun serveur de base de données n'est nécessaire, l'application utilise SQLite.

## Installation

Depuis la racine du projet (le dossier qui contient `main.py` et `alembic.ini`) :

```
pip install -r requirements.txt
```

> Toutes les commandes de ce document se lancent depuis cette racine. Si une commande comme `uvicorn` ou `alembic` n'est pas reconnue, la faire précéder de `python -m` (par exemple `python -m alembic upgrade head`).

## Configuration de la base de données

La base est un fichier SQLite nommé `library.db`, créé à la racine du projet.

## Exécution des migrations

Le schéma de la base est géré par Alembic. Les migrations sont dans `alembic/versions/` (schéma initial, évolution « genre » des ouvrages, puis ajustements sur les emprunts).

```
python -m alembic upgrade head
```

Cette commande crée la base si elle n'existe pas et applique toutes les migrations dans l'ordre. 

## Chargement des fixtures

Un jeu de données de test est fourni dans `fixtures.py`. Une fois la base créée :

```
python fixtures.py
```

Le script affiche : `Fixtures chargées : 5 auteurs, 10 ouvrages, 5 adhérents, 7 emprunts.`

Les données sont variées :

- des ouvrages avec un genre et d'autres sans genre ;
- un auteur avec trois ouvrages, d'autres avec un ou deux ;
- un adhérent avec plusieurs emprunts, un autre sans aucun emprunt ;
- 4 emprunts en cours (sans date de retour), dont un en retard, et 3 emprunts rendus ;
- des durées de prêt différentes (7, 14 et 21 jours) ;
- un même ouvrage emprunté plusieurs fois à des dates différentes.

Pour repartir de zéro :

```
del library.db
python -m alembic upgrade head
python fixtures.py
```

## Lancement de l'API

```
python -m uvicorn main:app --reload
```

L'API est disponible sur http://127.0.0.1:8000. La documentation est disponible sur http://127.0.0.1:8000/docs pour utiliser les différents routers.

## Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/authors` | Lister les auteurs |
| POST | `/authors` | Créer un auteur |
| GET | `/authors/{id}` | Consulter un auteur |
| GET | `/authors/{id}/books` | Ouvrages d'un auteur |
| GET | `/books` | Lister les ouvrages |
| POST | `/books` | Créer un ouvrage |
| GET | `/books/{id}` | Consulter un ouvrage |
| DELETE | `/books/{id}` | Supprimer un ouvrage |
| GET | `/members` | Lister les adhérents |
| POST | `/members` | Créer un adhérent |
| GET | `/members/{id}/loans` | Emprunts d'un adhérent |
| GET | `/loans` | Lister les emprunts |
| GET | `/loans/ongoing` | Emprunts en cours |
| POST | `/loans` | Créer un emprunt |
| PUT | `/loans/{id}/return` | Enregistrer le retour d'un ouvrage |

D'autres routes ont été ajoutées, elles permettent de suivre les emprunts en cours et d'enregistrer un retour.

## Exemples d'utilisation

Avec les fixtures chargées, ces exemples peuvent être essayés dans `/docs`.

Cas d'erreur à essayer :

| Requête | Réponse |
|---|---|
| `GET /authors/999` | 404, auteur introuvable |
| `POST /books` avec `"id_auteur": 999` | 404, auteur introuvable |
| `POST /loans` avec `"id_ouvrage": 1` (déjà emprunté) | 409, ouvrage déjà emprunté |
| `POST /loans` avec une `date_retour` avant `date_emprunt` | 422, dates incohérentes |
| `DELETE /books/1` | 409, l'ouvrage a des emprunts |

## Architecture et choix principaux

```
app/
├── models/         # tables SQLAlchemy (une classe par fichier)
├── repositories/   # accès à la base (une classe par entité)
├── routers/        # endpoints FastAPI 
├── schemas/        # modèles Pydantic
└── database.py     # connexion, session, Base
alembic/            # migrations
fixtures.py         # données de test
main.py             # création de l'application FastAPI
```

- **Séparation des responsabilités** : les routers reçoivent les requêtes et appliquent les règles métier ; les repositories contiennent toutes les requêtes à la base ; les modèles décrivent les tables ; les schémas décrivent les données échangées avec l'API. Un router n'écrit jamais de requête lui-même.
- **Suivi des emprunts** : un emprunt est « en cours » tant que sa `date_retour` est vide. La `duree` du prêt (en jours) est enregistrée avec l'emprunt ; la date limite de retour se calcule (`date_emprunt + duree`) et n'est pas stockée, pour éviter la redondance.
- **Suppression d'un ouvrage** : refusée s'il a des emprunts.
- **Codes HTTP** : 404 pour une ressource inexistante, 409 pour un conflit (ISBN ou email déjà utilisé, ouvrage déjà emprunté), 422 pour des données invalides.
