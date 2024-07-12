from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Bid
from app.schemas import (
    BidCreate,
    BidUpdate,
    BidUpdatePartial
)


async def get_bid(
        session: AsyncSession,
        bid_id: int | None
) -> Bid:

    return await session.get(Bid, bid_id)


async def create_bid(
        session: AsyncSession,
        bid: BidCreate,
        bidder_id: int
) -> Bid:
    bid = Bid(**bid.model_dump(), bidder_id=bidder_id)
    session.add(bid)
    await session.commit()
    return bid


async def update_bid(
        session: AsyncSession,
        bid: Bid,
        bid_update: BidUpdate | BidUpdatePartial,
        partial: bool = False
) -> Bid:
    for name, value in bid_update.model_dump(exclude_unset=partial).items():
        setattr(bid, name, value)

    await session.commit()
    return bid


async def delete_bid(
        session: AsyncSession,
        bid: Bid
) ->None:
    await session.delete(bid)
    await session.commit()