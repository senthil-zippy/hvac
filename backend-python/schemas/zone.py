from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ZoneCreate(BaseModel):
    floor_id: UUID
    name: str
    code: str
    area: float
    occupancy: int


class ZoneUpdate(BaseModel):
    name: str
    code: str
    area: float
    occupancy: int


class ZoneResponse(BaseModel):
    id: UUID
    floor_id: UUID
    name: str
    code: str
    area: float
    occupancy: int
    created_at: datetime
    updated_at: datetime
