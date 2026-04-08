import pytest
import uuid

from app.models.link import Link
from app.services.utils import generate_short_id


@pytest.mark.asyncio
async def test_create_short_success(client, db_session):
    data = {"original_url": f"https://example.com/{uuid.uuid4()}"}
    response = await client.post("/shorten", json=data)

    assert response.status_code == 201
    assert "short_id" in response.json()


@pytest.mark.asyncio
async def test_redirect_success(client, db_session):
    original_url = f"https://example.com/{uuid.uuid4()}"
    short_id = generate_short_id()

    new_link = Link(original_url=original_url, short_id=short_id)
    db_session.add(new_link)
    await db_session.flush()

    response = await client.get(f"/{short_id}")

    assert response.status_code == 307
    assert response.headers["location"] == original_url


@pytest.mark.asyncio
async def test_visit_counts_success(client, db_session):
    original_url = f"https://example.com/{uuid.uuid4()}"
    short_id = generate_short_id()

    new_link = Link(original_url=original_url, short_id=short_id)
    db_session.add(new_link)
    await db_session.flush()

    await client.get(f"/{short_id}")
    await client.get(f"/{short_id}")

    await db_session.refresh(new_link)

    assert new_link.visit_counts == 2


@pytest.mark.asyncio
async def test_redirect_failed(client):
    short_id = generate_short_id()
    response = await client.get(f"/{short_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_visit_counts_failed(client):
    short_id = generate_short_id()
    response = await client.get(f"/stats/{short_id}")

    assert response.status_code == 404
