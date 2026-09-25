from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class FormAnswers(Base):
    __tablename__ = "form_answers"

    id: Mapped[int] = mapped_column(primary_key=True)

    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="RESTRICT"),
        index=True,
    )

    answers: Mapped[str] = mapped_column(String(20))

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        index=True,
    )

    store: Mapped["Store"] = relationship(back_populates="answers")