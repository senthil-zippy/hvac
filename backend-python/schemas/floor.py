from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FloorCreate(BaseModel):
    building_id: UUID
    name: str
    code: str


class FloorUpdate(BaseModel):
    name: str
    code: str


class FloorResponse(BaseModel):
    id: UUID
    building_id: UUID
    name: str
    code: str
    created_at: datetime
    updated_at: datetime
