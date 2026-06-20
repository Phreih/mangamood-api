from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    manga_title: str = Field(..., min_length=1, description="Título del manga o manhwa")
    author: str = Field(..., min_length=1, description="Nombre de quien escribe la reseña")
    content: str = Field(..., min_length=1, description="Texto de la reseña")


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    manga_title: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None


class ReviewOut(ReviewBase):
    id: int
    mood: Optional[str] = None
    created_at: Optional[datetime] = None


class AnalyzeRequest(BaseModel):
    content: str = Field(..., min_length=1, description="Texto a analizar")


class AnalyzeResponse(BaseModel):
    content: str
    mood: str
