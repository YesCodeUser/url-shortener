import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.db.session import get_db
from app.core.config import settings


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    async with engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(bind=connection, expire_on_commit=False)

        yield session

        await session.close()
        await transaction.rollback()

    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
