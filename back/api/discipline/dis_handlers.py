from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from api.discipline.dis_models import ShowDiscipline
from api.discipline.dis_models import CreateDiscipline

from api.discipline.dis_servises import _create_new_discipline
from api.discipline.dis_servises import _get_all_discipline

from data_base.session import get_db
from data_base.db_models import Discipline


dis_router = APIRouter()


@dis_router.post("/create", response_model=ShowDiscipline)
async def create_discipline(body: CreateDiscipline, db: AsyncSession = Depends(get_db)) -> ShowDiscipline:
    try:
        return await _create_new_discipline(body, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка создания записи: {err}")


@dis_router.get("/get_all", response_model=List[ShowDiscipline])
async def get_all_discipline(db: AsyncSession = Depends(get_db)) -> List[ShowDiscipline]:
    try:
        discipline_list = await _get_all_discipline(db)
        return [ShowDiscipline(dis_id=discipline.dis_id, name=discipline.name) for discipline in discipline_list]
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка выгрузки записей: {err}")
