from pydantic import BaseModel, Field, field_validator

class AdherentCreate(BaseModel):
    nom: str = Field(min_length=3)
    prenom: str = Field(min_length=3)
    email: str

    @field_validator("name") 
    @classmethod 
    def clean_name(cls, value: str) -> str: 
        value = value.strip() 
        if len(value) < 3: 
            raise ValueError( 
            "Le nom doit contenir au moins 3 caractères." 
            ) 
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip()
        if "@" not in value:
            raise ValueError("L'email doit contenir un @.")
        return value