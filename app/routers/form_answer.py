from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.form_answers import (
    FormAnswers,
)
from app.models.stores import Store
from app.routers.stores import get_store_or_404
from app.schemas.form_answers import (
    FormAnswerSchema,
)
from app.templating import templates

router = APIRouter()

@router.get(path="/{store_slug}")
async def home(
    request: Request,
    store: Store = Depends(get_store_or_404),
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"store": store},
    )

@router.post(
    path="/{store_slug}/api/answer/",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar a resposta"
)
async def submit_answer(
    payload: FormAnswerSchema,
    store: Store = Depends(get_store_or_404),
    db: AsyncSession = Depends(get_session),
):
    answer = FormAnswers(
        store_id=store.id,
        answer=payload.answer,
    )

    db.add(answer)
    await db.commit()
    await db.refresh(answer)

    return {
        "success": True,
        "message": "Resposta recebida com sucesso!",
        "answer": answer.answer,
    }