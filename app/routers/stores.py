from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.stores import Store
from app.schemas.stores import (
    StoreListPublicSchema,
    StorePublicSchema,
)

router = APIRouter()

@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=StoreListPublicSchema,
    summary="Listar lojas",
)
async def list_stores(
    db: AsyncSession = Depends(get_session),
):
    result = await db.scalars(select(Store))
    stores = result.all()

    return {"stores": stores}

async def get_store_or_404(
    store_slug: str,
    db: AsyncSession = Depends(get_session),
) -> Store:
    result = await db.execute(
        select(Store).where(
            Store.slug == store_slug,
            Store.is_active.is_(True),
        )
    )

    store = result.scalar_one_or_none()

    if store is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada ou inativa",
        )

    return store