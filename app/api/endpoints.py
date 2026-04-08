from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.link import LinkRequest, LinkResponse, AmountVisitsResponse
from app.services.utils import generate_short_id
from app.models.link import Link
from app.db.session import get_db

router = APIRouter()


@router.post("/shorten", response_model=LinkResponse, status_code=201)
async def shorten_url(payload: LinkRequest, db: AsyncSession = Depends(get_db)):
    while True:
        short_id = generate_short_id()

        query = select(Link).where(Link.short_id == short_id)
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            break

    new_link = Link(original_url=str(payload.original_url), short_id=short_id)

    db.add(new_link)
    await db.commit()
    await db.refresh(new_link)

    return new_link


@router.get("/stats/{short_id}", response_model=AmountVisitsResponse)
async def get_amount_clicks(short_id: str, db: AsyncSession = Depends(get_db)):
    query = select(Link).where(Link.short_id == short_id)
    result = await db.execute(query)
    link = result.scalar_one_or_none()

    if not link:
        raise HTTPException(status_code=404)

    return link


@router.get("/{short_id}", status_code=307)
async def redirect_to_url(short_id: str, db: AsyncSession = Depends(get_db)):
    query = select(Link).where(Link.short_id == short_id)
    result = await db.execute(query)
    link: Link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404)

    text_query = text("UPDATE links SET visit_counts = visit_counts + 1 WHERE short_id = :s_id")
    await db.execute(text_query, {'s_id': short_id})
    await db.commit()

    return RedirectResponse(url=link.original_url)
