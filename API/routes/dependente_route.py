from fastapi import APIRouter, Request
from core.banco import banco
from schemas.dependente_schema import Dependente
from services.dependente_service import inscricaodep

router = APIRouter()

# Cria Dependente
@router.post("/dependente")
async def criadependente(dep: Dependente, request: Request):
    return inscricaodep(dep, banco, request)