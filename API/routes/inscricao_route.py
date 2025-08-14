from fastapi import APIRouter, Request
from core.banco import banco
from schemas.inscricao_schema import Inscricao
from services.inscricao_service import inscricao, deletapessoa, listainscricoes, totalinscricoes, totalpresenca, mudapresenca

router = APIRouter()

# Cria Inscrição
@router.post("/inscricao")
async def criainscricao(pessoa: Inscricao, request: Request):
    return inscricao(pessoa, banco, request)

@router.delete('/desativa/{id}')
async def desativapessoa(id: int, request: Request):
    user_ip = request.headers.get("X-Forwarded-For", "IP desconhecido")
    user_agent = request.headers.get("X-User-Agent", "Navegador desconhecido")

    return deletapessoa(id, banco, user_ip, user_agent)

@router.get("/inscricoes/{id}")
async def inscricoes(id: int):
    return listainscricoes(id, banco)

@router.get("/inscricoes")
async def totinscricoes():
    return totalinscricoes(banco)

@router.get("/presentes")
async def totpresencas():
    return totalpresenca(banco)

@router.put("/presenca/{id}")
async def changepresenca(id: int):
    return mudapresenca(id, banco)