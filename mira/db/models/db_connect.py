from litestar import Litestar
from litestar.datastructures import State
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import IntegrityError
from litestar.exceptions import ClientException
from db.models.models import Base
from litestar import status_codes

@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, 'engine', None)
    if engine is None:
        engine = create_async_engine('sqlite+aiosqlite:///miappe.db', echo=True)
        app.state.engine = engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)    
        
    try: 
        yield
    finally:
        await engine.dispose()

sessionmaker = async_sessionmaker(expire_on_commit=False)

async def provide_transaction(state: State) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker(bind=state.engine) as session:
        try:
            async with session.begin():
                yield session
        except IntegrityError as exc:
            raise ClientException(
                status_code=status_codes.HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc