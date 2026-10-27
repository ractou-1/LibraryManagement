from fastapi import FastAPI
 
from app.routers import auteur_router, ouvrage_router, adherent_router, emprunt_router
 
app = FastAPI(title="Médiathèque")
 
app.include_router(auteur_router.router)
app.include_router(ouvrage_router.router)
app.include_router(adherent_router.router)
app.include_router(emprunt_router.router)