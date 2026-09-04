#app/app.py
from typing import Annotated
from datetime import date

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession


import schemas

from dependencies import get_db_session
from lifespan import lifespan
from services import (
    create_advertisement,
    get_advertisement,
    update_advertisement,
    delete_advertisement,
    search_advertisements,
)

app = FastAPI(
    title="Advertisement API",
    description="API for managing advertisements",
    lifespan=lifespan,
    version="0.0.1"
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]

@app.post("/advertisement",
          response_model=schemas.CreateAdvertisementResponse,
          summary="Создать объявление",
          status_code=201,
          tags=["Создание объявления"],
          )
async def post_advert(
        session: SessionDep,
        advert_data: schemas.CreateAdvertisementRequest,
):
    new_advertisement = await create_advertisement(session, advert_data)
    return schemas.CreateAdvertisementResponse(id=new_advertisement.id)


@app.get("/advertisement",
         response_model=list[schemas.GetAdvertisementResponse],
         summary="Поиск объявлений",
         tags=["Поиск объявлений"],
         )
async def search_adverts(
        session: SessionDep,
        title: str | None = None,
        description: str | None = None,
        price: int | None = None,
        author: str | None = None,
        created_at: date | None = None,
):
    advertisements = await search_advertisements(
        session=session,
        title=title,
        description=description,
        price=price,
        author=author,
        created_at=created_at,
    )
    return [
        schemas.GetAdvertisementResponse(**advertisement.to_dict())
        for advertisement in advertisements
    ]


@app.get("/advertisement/{advertisement_id}",
         response_model=schemas.GetAdvertisementResponse,
         summary="Получить объявление",
         tags=["Получение объявления"],
         )
async def get_advert(
        session: SessionDep,
        advertisement_id: int,
):
    advertisement = await get_advertisement(session, advertisement_id)
    return schemas.GetAdvertisementResponse(**advertisement.to_dict())

@app.patch("/advertisement/{advertisement_id}",
          response_model=schemas.UpdateAdvertisementResponse,
          summary="Обновить объявление",
          tags=["Обновление объявления"],
          )
async def patch_advert(
        session: SessionDep,
        advertisement_id: int,
        update_data: schemas.UpdateAdvertisementRequest,
):
    updated_advertisement = await update_advertisement(session, advertisement_id, update_data)
    return schemas.UpdateAdvertisementResponse(**updated_advertisement.to_dict())

@app.delete("/advertisement/{advertisement_id}",
            response_model=schemas.OKResponse,
            summary="Удалить объявление",
            tags=["Удаление объявления"],
            )
async def delete_advert(
        session: SessionDep,
        advertisement_id: int,
):
    await delete_advertisement(session, advertisement_id)
    return schemas.OKResponse()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
