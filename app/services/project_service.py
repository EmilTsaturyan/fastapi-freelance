from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectUpdatePartial
)


async def get_project(
        session: AsyncSession,
        project_id: int | None
) -> Project:

    return await session.get(Project, project_id)


async def create_project(
        session: AsyncSession,
        project: ProjectCreate,
        user_id: int
) -> Project:
    project = Project(**project.model_dump(), user_id=user_id)
    session.add(project)
    await session.commit()
    return project


async def update_project(
        session: AsyncSession,
        project: Project,
        project_update: ProjectUpdate | ProjectUpdatePartial,
        partial: bool = False
) -> Project:
    for name, value in project_update.model_dump(exclude_unset=partial).items():
        setattr(project, name, value)

    await session.commit()
    return project


async def delete_project(
        session: AsyncSession,
        project: Project
) ->None:
    await session.delete(project)
    await session.commit()