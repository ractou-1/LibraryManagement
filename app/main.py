from fastapi import FastAPI
 
from app.routers import auteurs, ouvrages, adherents, emprunts
 
app = FastAPI(title="Médiathèque")
 
app.include_router(auteurs.router)
app.include_router(ouvrages.router)
app.include_router(adherents.router)
app.include_router(emprunts.router)
