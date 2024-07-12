from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import project_service
from app.utils import get_project_by_id, check_project_ownership, get_current_user
from app.models import User
from app.schemas import Project, ProjectCreate, ProjectUpdate, ProjectUpdatePartial
from app.db import database



router = APIRouter(tags=['Projects'])


@router.post('/', response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(database.session_dependency)
):
    return await project_service.create_project(session=session, project=project, user_id=user.id)


@router.get('/{project_id}', response_model=Project)
async def get_project(project: Project = Depends(get_project_by_id)):
    return project


@router.put('/{project_id}', response_model=Project)
async def update_project(
    project_update: ProjectUpdate,
    project: Project = Depends(check_project_ownership),
    session: AsyncSession = Depends(database.session_dependency)
):
    return await project_service.update_project(
        session=session,
        project=project,
        project_update=project_update,
        partial=False
    )
    

@router.patch('/{project_id}', response_model=Project)
async def update_project_partial(
    project_update: ProjectUpdatePartial,
    project: Project = Depends(check_project_ownership),
    session: AsyncSession = Depends(database.session_dependency)
):
    return await project_service.update_project(
        session=session,
        project=project,
        project_update=project_update,
        partial=True
    )


@router.delete('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    project: Project = Depends(check_project_ownership),
    session: AsyncSession = Depends(database.session_dependency)
):
    await session.delete(project)
    await session.commit()
