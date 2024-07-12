from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import bid_service
from app.utils import get_bid_by_id, get_current_user, get_project_by_id
from app.models import User
from app.schemas import Bid, BidCreate, BidUpdate, BidUpdatePartial
from app.db import database



router = APIRouter(tags=['Bids'])


@router.post('/', response_model=Bid, status_code=status.HTTP_201_CREATED)
async def create_bid(
    bid: BidCreate,
    session: AsyncSession = Depends(database.session_dependency),
    user: User = Depends(get_current_user)
):
    project = await get_project_by_id(project_id=bid.project_id, session=session)
    if project:
        return await bid_service.create_bid(session=session, bid=bid, bidder_id=user.id)


@router.get('/{bid_id}', response_model=Bid)
async def get_bid(bid: Bid = Depends(get_bid_by_id)):
    return bid


@router.put('/{bid_id}', response_model=Bid)
async def update_bid(
    bid_update: BidUpdate,
    bid: Bid = Depends(get_bid_by_id),
    session: AsyncSession = Depends(database.session_dependency)
):
    return await bid_service.update_bid(
        session=session,
        bid=bid,
        bid_update=bid_update,
        partial=False
    )
    

@router.patch('/{bid_id}', response_model=Bid)
async def update_bid_partial(
    bid_update: BidUpdatePartial,
    bid: Bid = Depends(get_bid_by_id),
    session: AsyncSession = Depends(database.session_dependency)
):
    return await bid_service.update_bid(
        session=session,
        bid=bid,
        bid_update=bid_update,
        partial=True
    )


@router.delete('/{bid_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_bid(
    bid: Bid = Depends(get_bid_by_id), 
    session: AsyncSession = Depends(database.session_dependency)
    ):
    await session.delete(bid)
    await session.commit()
    

