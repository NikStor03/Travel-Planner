from pydantic import Field
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class PlaceCreate(BaseModel):
    external_id: int = Field(..., gt=0)
    notes: Optional[str] = None

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    places: Optional[List[PlaceCreate]] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[str] = Field(default=None, description="YYYY-MM-DD")

class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None


class PlaceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    external_id: int
    title: Optional[str]
    notes: Optional[str]
    visited: bool
    visited_at: Optional[str]


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    start_date: Optional[str]
    completed: bool
    completed_at: Optional[str]
    places: List[PlaceOut]

