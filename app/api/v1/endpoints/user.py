from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.services import user_service
from app.schemas import UserCreate, UserResponse, UserLogin
from app.db import database
from app.utils import get_current_user


router = APIRouter(tags=['users'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, session: AsyncSession = Depends(database.session_dependency)):
    db_user = await user_service.get_user_by_email(session=session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Email already registred' 
        )
    return await user_service.create_user(session=session, user=user)


@router.post('/login')
async def login(user: UserLogin, session: AsyncSession = Depends(database.session_dependency)):
    authenticated_user = await user_service.authenticate_user(
        session=session,
        email=user.email,
        password=user.password
    )

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid credentials'
        )
    try:
        token = await user_service.create_token(session=session, user_id=authenticated_user.id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already logged in'
        )
    return {'token': token.token}


@router.get('/me', response_model=UserResponse)
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.delete('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(token: str = Header(None), session: AsyncSession = Depends(database.session_dependency)):
    await user_service.delete_token(session=session, token=token)



