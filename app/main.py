import sys
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import Base, database
from app.api.v1 import router




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)