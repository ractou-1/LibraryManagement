from datetime import date
from pydantic import BaseModel, Field, model_validator

class EmpruntCreate(BaseModel):
    id_adherent: int
    id_ouvrage: int
    duree: int = Field(gt=0)
    date_emprunt: date
    date_retour: date = None

    # Règle métier : le retour ne peut pas être avant le début de l'emprunt
    @model_validator(mode="after")
    def validate_dates(self):
        if self.date_retour is not None and self.date_retour < self.date_emprunt:
            raise ValueError(
                "La date de retour ne peut pas être antérieure à la date d'emprunt."
            )
        return self