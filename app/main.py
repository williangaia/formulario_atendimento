from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Formulário de Satissfação")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static", 
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")

class SatisfactionRequest(BaseModel):
    answer: str = Field(pattern="^(ruim|bom|otimo)$")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@app.post("/api/satisfaction/")
async def submit_satisfaction(payload: SatisfactionRequest):
    # Adiconar persistência de dados

    return {
        "success": True,
        "message": "Resposta recebida com sucesso!",
        "answer": payload.answer,
    }