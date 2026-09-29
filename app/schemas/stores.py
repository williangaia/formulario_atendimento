from pydantic import BaseModel

class StoreSchema(BaseModel):
    nroempresa: int
    slug: str
    name: str
    is_active: bool = True

class StorePublicSchema(BaseModel):
    id: int
    nroemprsa: int
    slug: str
    name: str
    is_active: bool

class StoreListPublicSchema(BaseModel):
    stores: list[StorePublicSchema]