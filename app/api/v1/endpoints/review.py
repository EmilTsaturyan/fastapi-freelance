from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import review_service
from app.utils import get_review_by_id, get_current_user, get_project_by_id
from app.models import User
from app.schemas import Review, ReviewCreate, ReviewUpdate, ReviewUpdatePartial
from app.db import database


router = APIRouter(tags=['Reviews'])


@router.post('/', response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_post(
    review: ReviewCreate,
    session: AsyncSession = Depends(database.session_dependency),
    user: User = Depends(get_current_user)
):
    project = await get_project_by_id(project_id=review.project_id, session=session)
    if project:
        return await review_service.create_review(session=session, review=review, reviewer_id=user.id)
    

@router.get('/{review_id}', response_model=Review)
async def get_review(review: Review = Depends(get_review_by_id)):
    return review


@router.put('/{review_id}', response_model=Review)
async def update_review(
    review_update: ReviewUpdate,
    review: Review = Depends(get_review_by_id),
    session: AsyncSession = Depends(database.session_dependency)
):
    return await review_service.update_review(
        session=session,
        review=review,
        review_update=review_update,
        partial=False
    )


@router.patch('/{review_id}', response_model=Review)
async def update_review_partial(
    review_update: ReviewUpdatePartial,
    review: Review = Depends(get_review_by_id),
    session: AsyncSession = Depends(database.session_dependency)
):
    return await review_service.update_review(
        session=session,
        review=review,
        review_update=review_update,
        partial=True
    )


@router.delete('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review: Review = Depends(get_review_by_id), 
    session: AsyncSession = Depends(database.session_dependency)
    ):
    await session.delete(review)
    await session.commit()
    

