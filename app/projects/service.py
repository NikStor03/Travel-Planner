from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.aic.client import AICClient
from app.common.errors import bad_request, conflict, not_found
from app.projects.models import Project, ProjectPlace
from app.projects.repository import ProjectRepository
from app.places.repository import PlaceRepository
from app.projects.schemas import ProjectCreate, ProjectUpdate

MAX_PLACES = 10
MIN_PLACES = 1

class ProjectService:
    def __init__(self, project_repo: ProjectRepository, place_repo: PlaceRepository, aic: AICClient):
        self.project_repo = project_repo
        self.place_repo = place_repo
        self.aic = aic

    async def create_project(self, db: Session, payload: ProjectCreate) -> Project:
        places_payload = payload.places or []
        if places_payload and (len(places_payload) < MIN_PLACES or len(places_payload) > MAX_PLACES):
            bad_request(f"Project must include between {MIN_PLACES} and {MAX_PLACES} places when places array is provided.")

        project = Project(
            name=payload.name,
            description=payload.description,
            start_date=payload.start_date,
        )

        if places_payload:
            seen = set()
            for p in places_payload:
                if p.external_id in seen:
                    bad_request("Duplicate external_id in places array.")
                seen.add(p.external_id)

            for p in places_payload:
                art = await self.aic.get_artwork(p.external_id)
                if not art:
                    bad_request(f"External place {p.external_id} not found in Art Institute API.")
                project.places.append(ProjectPlace(
                    external_id=p.external_id,
                    title=art.get("title"),
                    notes=p.notes,
                    visited=False,
                ))

        return self.project_repo.create(db, project)

    def list_projects(self, db: Session, offset: int, limit: int, status: str | None):
        return self.project_repo.list(db, offset=offset, limit=limit, status=status)

    def get_project(self, db: Session, project_id: int) -> Project:
        project = self.project_repo.get(db, project_id)
        if not project:
            not_found("Project not found.")
        return project

    def update_project(self, db: Session, project_id: int, payload: ProjectUpdate) -> Project:
        project = self.get_project(db, project_id)
        if payload.name is not None:
            project.name = payload.name
        if payload.description is not None:
            project.description = payload.description
        if payload.start_date is not None:
            project.start_date = payload.start_date
        return self.project_repo.update(db, project)

    def delete_project(self, db: Session, project_id: int) -> None:
        project = self.get_project(db, project_id)
        if self.project_repo.has_visited_places(db, project_id):
            conflict("Project cannot be deleted because it contains visited places.")
        self.project_repo.delete(db, project)

    def recompute_completion(self, db: Session, project: Project) -> Project:
        # completed if >=1 place and all visited
        if not project.places:
            project.completed = False
            project.completed_at = None
            return self.project_repo.update(db, project)

        all_visited = all(p.visited for p in project.places)
        project.completed = bool(all_visited)
        project.completed_at = datetime.now(timezone.utc).isoformat() if all_visited else None
        return self.project_repo.update(db, project)
