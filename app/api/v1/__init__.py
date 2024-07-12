from fastapi import APIRouter

from .endpoints import (
    project_router, 
    bid_router, 
    review_router,
    user_router
    )


router = APIRouter()
router.include_router(project_router, prefix='/projects')
router.include_router(bid_router, prefix='/bids')
router.include_router(review_router, prefix='/reviews')
router.include_router(user_router, prefix='/users')
