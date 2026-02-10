from sqlalchemy.orm import Session
from sqlalchemy import select
from app.projects.models import ProjectPlace

class PlaceRepository:
    def create(self, db: Session, place: ProjectPlace) -> ProjectPlace:
        db.add(place)
        db.commit()
        db.refresh(place)
        return place

    def list_for_project(self, db: Session, project_id: int):
        stmt = select(ProjectPlace).where(ProjectPlace.project_id == project_id)
        return db.scalars(stmt).all()

    def get_in_project(self, db: Session, project_id: int, place_id: int) -> ProjectPlace | None:
        stmt = select(ProjectPlace).where(
            ProjectPlace.project_id == project_id,
            ProjectPlace.id == place_id
        )
        return db.scalars(stmt).first()

    def update(self, db: Session, place: ProjectPlace) -> ProjectPlace:
        db.add(place)
        db.commit()
        db.refresh(place)
        return place

    def exists_external_in_project(self, db: Session, project_id: int, external_id: int) -> bool:
        stmt = select(ProjectPlace.id).where(
            ProjectPlace.project_id == project_id,
            ProjectPlace.external_id == external_id
        )
        return db.execute(stmt).first() is not None
