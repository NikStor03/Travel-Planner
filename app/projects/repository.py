from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.projects.models import Project, ProjectPlace

class ProjectRepository:
    def create(self, db: Session, project: Project) -> Project:
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    def get(self, db: Session, project_id: int) -> Project | None:
        return db.get(Project, project_id)

    def list(self, db: Session, offset: int, limit: int, status: str | None):
        stmt = select(Project)
        if status == "completed":
            stmt = stmt.where(Project.completed == True)
        elif status == "active":
            stmt = stmt.where(Project.completed == False)
        stmt = stmt.offset(offset).limit(limit)
        return db.scalars(stmt).all()

    def update(self, db: Session, project: Project) -> Project:
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    def delete(self, db: Session, project: Project) -> None:
        db.delete(project)
        db.commit()

    def has_visited_places(self, db: Session, project_id: int) -> bool:
        stmt = select(func.count()).select_from(ProjectPlace).where(
            ProjectPlace.project_id == project_id,
            ProjectPlace.visited == True,
        )
        return (db.execute(stmt).scalar_one() or 0) > 0

    def count_places(self, db: Session, project_id: int) -> int:
        stmt = select(func.count()).select_from(ProjectPlace).where(ProjectPlace.project_id == project_id)
        return int(db.execute(stmt).scalar_one() or 0)
