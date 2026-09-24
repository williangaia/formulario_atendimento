from datetime import datetime

from pydantic import BaseModel, Field

class FormAnswerSchema(BaseModel):
    answer: str = Field(pattern="^(ruim|bom|excelente)$")

class FormAnswerPublicSchema(BaseModel):
    id: int
    store_id: int
    answer: str
    created_at: datetime

class FormAnswerListPublicSchema(BaseModel):
    answers: list[FormAnswerPublicSchema]