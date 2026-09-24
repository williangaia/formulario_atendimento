from pydantic import BaseModel

class StoreSchema(BaseModel):
    slug: str
    name: str

class StorePublicSchema(BaseModel):
    id: int
    slug: str
    name: str
    is_active: bool

class StoreListPublicSchema(BaseModel):
    stores: list[StorePublicSchema]