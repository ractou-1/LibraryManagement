from datetime import date

from pydantic import BaseModel, Field, field_validator

class AuteurCreate(BaseModel):
    nom: str = Field(min_length=3)
    prenom: str = Field(min_length=3)
    date_naissance: date = None

    @field_validator("nom") 
    @classmethod 
    def clean_name(cls, value: str) -> str: 
        value = value.strip() 
        if len(value) < 3: 
            raise ValueError( 
            "Le nom doit contenir au moins 3 caractères." 
            ) 
        return value

    @field_validator("prenom") 
    @classmethod 
    def clean_name(cls, value: str) -> str: 
        value = value.strip() 
        if len(value) < 3: 
            raise ValueError( 
            "Le nom doit contenir au moins 3 caractères." 
            ) 
        return value 