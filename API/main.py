from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes.inscricao_route import router as inscricao_router
from routes.dependente_route import router as dependente_router

origins = [
    "https://dominio.com.br",
    "http://localhost:4200", 
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inscricao_router)
app.include_router(dependente_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5100, log_level="debug")