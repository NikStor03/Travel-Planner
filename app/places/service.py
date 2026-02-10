from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.aic.client import AICClient
from app.common.errors import bad_request, conflict, not_found
from app.projects.repository import ProjectRepository
from app.projects.service import MAX_PLACES
from app.places.repository import PlaceRepository
from app.projects.models import ProjectPlace
from app.projects.schemas import PlaceUpdate

class PlaceService:
    def __init__(self, project_repo: ProjectRepository, place_repo: PlaceRepository, aic: AICClient):
        self.project_repo = project_repo
        self.place_repo = place_repo
        self.aic = aic

    async def add_place(self, db: Session, project_id: int, external_id: int, notes: str | None) -> ProjectPlace:
        project = self.project_repo.get(db, project_id)
        if not project:
            not_found("Project not found.")

        count = self.project_repo.count_places(db, project_id)
        if count >= MAX_PLACES:
            bad_request(f"Project cannot have more than {MAX_PLACES} places.")

        if self.place_repo.exists_external_in_project(db, project_id, external_id):
            conflict("This external place is already in the project.")

        art = await self.aic.get_artwork(external_id)
        if not art:
            bad_request(f"External place {external_id} not found in Art Institute API.")

        place = ProjectPlace(
            project_id=project_id,
            external_id=external_id,
            title=art.get("title"),
            notes=notes,
            visited=False,
        )

        try:
            created = self.place_repo.create(db, place)
        except IntegrityError:
            # covers race cases on unique constraint
            conflict("This external place is already in the project.")
        return created

    def list_places(self, db: Session, project_id: int):
        project = self.project_repo.get(db, project_id)
        if not project:
            not_found("Project not found.")
        return self.place_repo.list_for_project(db, project_id)

    def get_place(self, db: Session, project_id: int, place_id: int) -> ProjectPlace:
        place = self.place_repo.get_in_project(db, project_id, place_id)
        if not place:
            not_found("Place not found in project.")
        return place

    def update_place(self, db: Session, project_id: int, place_id: int, payload: PlaceUpdate) -> ProjectPlace:
        place = self.get_place(db, project_id, place_id)

        if payload.notes is not None:
            place.notes = payload.notes
        if payload.visited is not None:
            place.visited = payload.visited
            place.visited_at = datetime.now(timezone.utc).isoformat() if payload.visited else None

        return self.place_repo.update(db, place)
