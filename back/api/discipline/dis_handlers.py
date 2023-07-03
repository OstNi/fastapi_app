from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from api.discipline.dis_models import ShowDiscipline
from api.discipline.dis_models import CreateDiscipline
from api.discipline.dis_models import UpdateDisciplineRequest

from api.discipline.dis_servises import _create_new_discipline
from api.discipline.dis_servises import _get_all_discipline
from api.discipline.dis_servises import _delete_discipline
from api.discipline.dis_servises import _update_discipline

from data_base.session import get_db


dis_router = APIRouter()


@dis_router.post("/post-create-dis", response_model=ShowDiscipline)
async def create_discipline(body: CreateDiscipline, db: AsyncSession = Depends(get_db)) -> ShowDiscipline:
    try:
        return await _create_new_discipline(body, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка создания записи: {err}")


@dis_router.get("/get-all-discipline-list", response_model=List[ShowDiscipline])
async def get_all_disciplines(db: AsyncSession = Depends(get_db)) -> List[ShowDiscipline]:
    try:
        discipline_list = await _get_all_discipline(db)
        return discipline_list
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка выгрузки записей: {err}")


@dis_router.delete("/delete-discipline/{dis_id}", response_model=ShowDiscipline)
async def delete_discipline(dis_id: int, db: AsyncSession = Depends(get_db)) -> ShowDiscipline:
    try:
        deleted_discipline = await _delete_discipline(dis_id, db)
        if deleted_discipline is not None:
            return deleted_discipline
        else:
            raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка удаления записи: {err}")


@dis_router.patch("/patch-discipline/{dis_id}", response_model=ShowDiscipline)
async def update_discipline(
        dis_id: int,
        body: UpdateDisciplineRequest,
        db: AsyncSession = Depends(get_db)
) -> ShowDiscipline | None:
    try:
        updated_discipline = await _update_discipline(dis_id, db, name=body.name)
        if updated_discipline is not None:
            return updated_discipline
        else:
            raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка обновление записи: {err}")