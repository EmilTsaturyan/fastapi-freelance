import uuid
import anyio.to_thread
from passlib.context import CryptContext
import anyio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User, Token
from app.schemas import (
    UserCreate,
    UserUpdate,
    UserUpdatePartial,
    UserResponse
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_password_hash(password: str) -> str:
    return await anyio.to_thread.run_sync(pwd_context.hash, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await anyio.to_thread.run_sync(pwd_context.verify, plain_password, hashed_password)


async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def authenticate_user(session: AsyncSession, email: str, password: str):
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not await verify_password(password, user.hashed_password):
        return None
    return user


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    hashed_password = await get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(db_user)
    await session.commit()
    return db_user


async def get_user_by_token(session: AsyncSession, token: str) -> Token:
    result = await session.execute(select(Token).filter(Token.token == token))
    return result.scalars().first()


async def create_token(session: AsyncSession, user_id: int) -> Token:
    token = str(uuid.uuid4())
    token = Token(token=token, user_id=user_id)
    session.add(token)
    await session.commit()
    return token


async def delete_token(session: AsyncSession, token: str):
    token = await get_user_by_token(session=session, token=token)
    if token:
        await session.delete(token)
        await session.commit()

