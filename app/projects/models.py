from sqlalchemy import String, Date, DateTime, ForeignKey, UniqueConstraint, func, Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[str | None] = mapped_column(String(10), nullable=True)

    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    completed_at: Mapped[str | None] = mapped_column(String(32), nullable=True)

    created_at: Mapped[str] = mapped_column(String(32), nullable=False, default=lambda: str(func.now()))
    updated_at: Mapped[str] = mapped_column(String(32), nullable=False, default=lambda: str(func.now()), onupdate=lambda: str(func.now()))

    places: Mapped[list["ProjectPlace"]] = relationship(back_populates="project", cascade="all, delete-orphan")

class ProjectPlace(Base):
    __tablename__ = "project_places"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="uq_project_external_place"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    external_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    visited: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    visited_at: Mapped[str | None] = mapped_column(String(32), nullable=True)

    project: Mapped["Project"] = relationship(back_populates="places")
