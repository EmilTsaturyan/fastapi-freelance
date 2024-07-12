from fastapi import Path, Header, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import database
from app.models import Project, Bid, Review, User
from app.services.user_service import get_user_by_token



async def get_entity_by_id(
    entity_class: object,
    entity_id: int,
    session: AsyncSession
) -> object:
    """
    Generic function to get an entity by its ID.
    
    :param entity_class: The SQLAlchemy model class of the entity.
    :param entity_id: The ID of the entity to retrieve.
    :param session: The SQLAlchemy AsyncSession for database access.
    :return: The entity if found, otherwise raises HTTPException.
    """
    entity = await session.get(entity_class, entity_id)

    if entity:
        return entity
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{entity_class.__name__} with id {entity_id} not found!'
    )


async def get_project_by_id(
        project_id: int = Path(...),
        session: AsyncSession = Depends(database.session_dependency)
) -> Project:
    return await get_entity_by_id(Project, project_id, session)


async def get_bid_by_id(
        bid_id: int = Path(...),
        session: AsyncSession = Depends(database.session_dependency)
) -> Bid:
    return await get_entity_by_id(Bid, bid_id, session)


async def get_review_by_id(
        review_id: int = Path(...),
        session: AsyncSession = Depends(database.session_dependency)
) -> Review:
    return await get_entity_by_id(Review, review_id, session)



async def get_current_user(
        token = Header(None), 
        session: AsyncSession = Depends(database.session_dependency)
    ):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token missing'
        )
    
    token = await get_user_by_token(session=session, token=token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )

    user = await session.get(User, token.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    return user


async def check_ownership(
        entity_class: object,
        entity_id: int,
        user_id_field: str,
        user: User,
        session: AsyncSession
) -> object:
    entity = await get_entity_by_id(entity_class, entity_id, session)
    
    if getattr(entity, user_id_field) != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not enougth permission for editing this {entity_class.__name__}'
        )
    return entity


async def check_project_ownership(
        project_id: int, 
        user: User = Depends(get_current_user),
        sesison: AsyncSession = Depends(database.session_dependency)
) -> Project:
    return await check_ownership(Project, project_id, 'user_id', user, sesison)
    

async def check_review_ownership(
        review_id: int, 
        user: User = Depends(get_current_user),
        sesison: AsyncSession = Depends(database.session_dependency)
) -> Review:
    return await check_ownership(Review, review_id, 'reviewer_id', user, sesison)
    

async def check_bid_ownership(
        bid_id: int, 
        user: User = Depends(get_current_user),
        sesison: AsyncSession = Depends(database.session_dependency)
) -> Bid:
    return await check_ownership(Bid, bid_id, 'user_id', user, sesison)
    
