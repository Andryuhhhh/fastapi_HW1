#app/schemas.py

from pydantic import BaseModel
from typing import Optional

class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: int
    author: str

class CreateAdvertisementResponse(BaseModel):
    id: int

class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    author: str
    created_at: Optional[str] = None

class UpdateAdvertisementRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    author: Optional[str] = None

class UpdateAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    author: str
    created_at: Optional[str] = None

class OKResponse(BaseModel):
    status: str = "ok"