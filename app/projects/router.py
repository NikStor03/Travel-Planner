from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.aic.client import AICClient
from app.projects.repository import ProjectRepository
from app.places.repository import PlaceRepository
from app.projects.service import ProjectService
from app.projects.schemas import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])

def get_service():
    return ProjectService(ProjectRepository(), PlaceRepository(), AICClient())

@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, db: Session = Depends(get_db), svc: ProjectService = Depends(get_service)):
    project = await svc.create_project(db, payload)
    project = svc.recompute_completion(db, project)
    return project

@router.get("", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    svc: ProjectService = Depends(get_service),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: str | None = Query(None, pattern="^(active|completed)$")
):
    return svc.list_projects(db, offset=offset, limit=limit, status=status_filter)

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), svc: ProjectService = Depends(get_service)):
    return svc.get_project(db, project_id)

@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db), svc: ProjectService = Depends(get_service)):
    return svc.update_project(db, project_id, payload)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db), svc: ProjectService = Depends(get_service)):
    svc.delete_project(db, project_id)
    return None
