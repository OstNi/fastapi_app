from enum import Enum
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import schemas
import crud

from data_base.session import get_db

import uuid

import time

dis_router = APIRouter()


@dis_router.post("/post-create-dis", response_model=schemas.ShowDiscipline)
async def create_discipline(
        discipline_in: schemas.CreateDiscipline,
        db: AsyncSession = Depends(get_db)
) -> schemas.ShowDiscipline:
    """
       Create an item with all the information:

       - **name**: each discipline must have a name
    """
    try:
        return await crud.discipline.create(db=db, obj_in=discipline_in)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка создания записи: {err.orig}")
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")


@dis_router.get("/get-disciplines-list", response_model=List[schemas.ShowDiscipline])
async def get_disciplines(
        db: AsyncSession = Depends(get_db),
        skip: int | None = None,
        limit: int | None = None
) -> List[schemas.ShowDiscipline]:
    """
    Получение списка дисциплин
    - **skip** - смещение
    - **limit** - количество записей
    """
    try:
        discipline_list = await crud.discipline.get_multi(db, skip=skip, limit=limit)
        return [schemas.ShowDiscipline(dis_id=item.dis_id, name=item.name) for item in discipline_list]
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка выгрузки записей: {err.orig}")
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")@dis_router.get("/get-disciplines-list", response_model=List[schemas.ShowDiscipline])
async def get_disciplines(
        db: AsyncSession = Depends(get_db),
        skip: int | None = None,
        limit: int | None = None
) -> List[schemas.ShowDiscipline]:
    """
    Получение списка дисциплин
    - **skip** - смещение
    - **limit** - количество записей
    """
    try:
        discipline_list = await crud.discipline.get_multi(db, skip=skip, limit=limit)
        return [schemas.ShowDiscipline(dis_id=item.dis_id, name=item.name) for item in discipline_list]
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка выгрузки записей: {err.orig}")
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")


@dis_router.get("/get-discipline/{dis_id}", response_model=schemas.ShowDiscipline)
async def get_discipline_by_id(dis_id: int, db: AsyncSession = Depends(get_db)) -> schemas.ShowDiscipline:
    try:
        discipline = await crud.discipline.get(db, obj_id=dis_id)
        if discipline is not None:
            return schemas.ShowDiscipline(
                dis_id=discipline.dis_id,
                name=discipline.name
            )
        else:
            raise HTTPException(status_code=400, detail=f"Записи с таким id не существует")
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка получения записи: {err}")
    except HTTPException as err:
        raise err
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")


@dis_router.delete("/delete-discipline/{dis_id}")
async def delete_discipline(dis_id: int, db: AsyncSession = Depends(get_db)):
    try:
        deleted_rows_cnt = await crud.discipline.remove(db, obj_id=dis_id)
        return {"code": 200, "deleted rows count": deleted_rows_cnt}
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка удаления записи: {err}")
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")


@dis_router.patch("/patch-discipline/{dis_id}")
async def update_discipline(
        dis_id: int,
        body: schemas.UpdateDiscipline,
        db: AsyncSession = Depends(get_db)
):
    try:
        updated_row_cnt = await crud.discipline.update(db, obj_id=dis_id, obj_in=body)
        return {"code": 200, "updated rows count": updated_row_cnt}
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка обновление записи: {err}")
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")


def prepare_data(num: int) -> List[schemas.CreateDiscipline]:
    return [schemas.CreateDiscipline(name=str(uuid.uuid4())) for _ in range(num)]


@dis_router.post('/create-test')
async def start_create_test(
        num: int,
        db: AsyncSession = Depends(get_db)):
    insert_data = prepare_data(num)

    start_time = time.time()
    ins_num = await create_disciplines(insert_data, db)
    end_time = time.time()
    execution_time = end_time - start_time
    return {
        'code': 200,
        'number of records inserted': ins_num,
        'time of execution': execution_time
    }


@dis_router.post("/post-create-dis-multi/{version}")
async def create_disciplines(
        disciplines_list: List[schemas.CreateDiscipline],
        db: AsyncSession = Depends(get_db),
) -> int:
    """
       Create an item with all the information:

       - **name**: each discipline must have a name
    """
    try:
        return await crud.discipline.create_multi(db=db, objs_in=disciplines_list)

    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка создания записи: {err.orig}")
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")
