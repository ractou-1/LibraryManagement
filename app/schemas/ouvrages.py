from pydantic import BaseModel, Field, field_validator

class OuvrageCreate(BaseModel):
    titre: str = Field(min_length=3)
    isbn: str = Field(min_length=1)
    annee_publication: int = Field(gt=0)
    genre: str = None
    id_auteur: int

    @field_validator("titre") 
    @classmethod 
    def clean_name(cls, value: str) -> str: 
        value = value.strip() 
        if len(value) < 3: 
            raise ValueError( 
            "Le titre doit contenir au moins 3 caractères." 
            ) 
        return value