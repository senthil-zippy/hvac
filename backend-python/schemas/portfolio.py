from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PortfolioCreate(BaseModel):
    name: str
    code: str


class PortfolioUpdate(BaseModel):
    name: str
    code: str


class PortfolioResponse(BaseModel):
    id: UUID
    name: str
    code: str
    created_at: datetime
    updated_at: datetime
