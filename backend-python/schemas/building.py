from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BuildingCreate(BaseModel):
    portfolio_id: UUID
    name: str
    code: str
    address: str


class BuildingUpdate(BaseModel):
    name: str
    code: str
    address: str


class BuildingResponse(BaseModel):
    id: UUID
    portfolio_id: UUID
    name: str
    code: str
    address: str
    created_at: datetime
    updated_at: datetime
