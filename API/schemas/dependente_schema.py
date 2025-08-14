from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date

class Dependente(BaseModel):
    idpai: int
    nome: str
    datanas: date
    telefone: Optional[str] = None
    email: Optional[EmailStr]
    membro: int
    presenca: Optional[int] = 0
    ativo: Optional[int] = 1

    @field_validator("email", mode="before")
    def email_vazio_para_none(cls, v):
        if v == "":
            return None
        return v
    
