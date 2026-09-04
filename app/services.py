#app/services.py
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas

async def create_advertisement(
        session: AsyncSession,
        advertisement: schemas.CreateAdvertisementRequest
):
    new_advertisement = models.Advertisement(**advertisement.model_dump())
    session.add(new_advertisement)
    await session.commit()
    await session.refresh(new_advertisement)
    return new_advertisement

async def get_advertisement(
        session: AsyncSession,
        advertisement_id: int
):
    stmt = select(models.Advertisement).where(models.Advertisement.id == advertisement_id)
    result = await session.execute(stmt)
    advertisement = result.scalar_one_or_none()
    if advertisement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Advertisement with id {advertisement_id} not found"
        )
    return advertisement

async def update_advertisement(
        session: AsyncSession,
        advertisement_id: int,
        update_data: schemas.UpdateAdvertisementRequest
) -> models.Advertisement:
    advertisement = await get_advertisement(session, advertisement_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(advertisement, key, value)

    await session.commit()
    await session.refresh(advertisement)

    return advertisement

async def delete_advertisement(
        session: AsyncSession,
        advertisement_id: int
) -> None:
    data = await get_advertisement(session, advertisement_id)
    await session.delete(data)
    await session.commit()
