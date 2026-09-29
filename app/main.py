from pathlib import Path

from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles

from app.routers import form_answer, stores

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Formulário de Satissfação")

@app.get("/health_check", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "OK"}

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static", 
)

app.include_router(
    router=stores.router,
    prefix="/api/v1/stores",
    tags=["stores"],
)

app.include_router(
    router=form_answer.router,
    tags=["form_answer"]
)