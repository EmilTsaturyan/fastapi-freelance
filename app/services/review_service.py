from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Review
from app.schemas import (
    ReviewCreate,
    ReviewUpdate,
    ReviewUpdatePartial
)


async def get_review(
        session: AsyncSession,
        review_id: int | None
) -> Review:

    return await session.get(Review, review_id)


async def create_review(
        session: AsyncSession,
        review: ReviewCreate,
        reviewer_id: int
) -> Review:
    review = Review(**review.model_dump(), reviewer_id=reviewer_id)
    session.add(review)
    await session.commit()
    return review


async def update_review(
        session: AsyncSession,
        review: Review,
        review_update: ReviewUpdate | ReviewUpdatePartial,
        partial: bool = False
) -> Review:
    for name, value in review_update.model_dump(exclude_unset=partial).items():
        setattr(review, name, value)

    await session.commit()
    return review


async def delete_review(
        session: AsyncSession,
        review: Review
) ->None:
    await session.delete(review)
    await session.commit()