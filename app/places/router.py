from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.aic.client import AICClient
from app.projects.repository import ProjectRepository
from app.places.repository import PlaceRepository
from app.places.service import PlaceService
from app.projects.service import ProjectService
from app.projects.schemas import PlaceOut, PlaceUpdate

router = APIRouter(prefix="/projects/{project_id}/places", tags=["places"])

class AddPlaceBody(BaseModel):
    external_id: int = Field(..., gt=0)
    notes: str | None = None

def get_place_svc():
    return PlaceService(ProjectRepository(), PlaceRepository(), AICClient())

def get_project_svc():
    return ProjectService(ProjectRepository(), PlaceRepository(), AICClient())

@router.post("", response_model=PlaceOut, status_code=status.HTTP_201_CREATED)
async def add_place(
    project_id: int,
    body: AddPlaceBody,
    db: Session = Depends(get_db),
    place_svc: PlaceService = Depends(get_place_svc),
):
    return await place_svc.add_place(db, project_id, body.external_id, body.notes)

@router.get("", response_model=list[PlaceOut])
def list_places(
    project_id: int,
    db: Session = Depends(get_db),
    place_svc: PlaceService = Depends(get_place_svc),
):
    return place_svc.list_places(db, project_id)

@router.get("/{place_id}", response_model=PlaceOut)
def get_place(
    project_id: int,
    place_id: int,
    db: Session = Depends(get_db),
    place_svc: PlaceService = Depends(get_place_svc),
):
    return place_svc.get_place(db, project_id, place_id)

@router.patch("/{place_id}", response_model=PlaceOut)
def update_place(
    project_id: int,
    place_id: int,
    payload: PlaceUpdate,
    db: Session = Depends(get_db),
    place_svc: PlaceService = Depends(get_place_svc),
    project_svc: ProjectService = Depends(get_project_svc),
):
    place = place_svc.update_place(db, project_id, place_id, payload)

    project = project_svc.get_project(db, project_id)
    project_svc.recompute_completion(db, project)

    return place
