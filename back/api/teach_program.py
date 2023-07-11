from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import schemas
import crud

from data_base.session import get_db


teach_program_router = APIRouter()


@teach_program_router.get("/get-teach_prog-list", response_model=List[schemas.ShowTeachProgram])
async def get_teach_programs(
        db: AsyncSession = Depends(get_db),
        skip: int | None = None,
        limit: int | None = None
) -> List[schemas.ShowTeachProgram]:
    """
    Получение списка дисциплин
    - **skip** - смещение
    - **limit** - количество записей
    """
    try:
        teach_program_list = await crud.teach_program.get_multi(db, skip=skip, limit=limit)
        return [schemas.ShowTeachProgram(
            tpr_id=item.tpr_id,
            confirm_date=item.confirm_date,
            status=item.status,
            protocol=item.protocol,
            practice_form=item.practice_form,
            practice_schedule=item.practice_schedule,
            info=item.info,
            dis_dis_id=item.dis_dis_id,
            tpt_tpt_id=item.tpt_tpt_id,
            dis_dis=item.dis_dis,
            tpt_tpt=item.tpt_tpt
        ) for item in teach_program_list]
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка выгрузки записей: {err.orig}")
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")


@teach_program_router.patch("/patch-teach_program-update/{tpr_id}", response_model=dict | None)
async def update_teach_program(
        tpr_id: int,
        body: schemas.UpdateTeachProgram,
        db: AsyncSession = Depends(get_db)
):
    try:
        updated_row_cnt = await crud.teach_program.update(db, obj_id=tpr_id, obj_in=body)
        return {"code": 200, "updated rows count": updated_row_cnt}
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка обновление записи: {err}")
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")


@teach_program_router.get("/get-teach_program/{tpt_id}", response_model=schemas.ShowTeachProgram)
async def get_discipline_by_id(tpt_id: int, db: AsyncSession = Depends(get_db)) -> schemas.ShowTeachProgram:
    try:
        teach_program = await crud.teach_program.get(db, obj_id=tpt_id)
        if teach_program is not None:
            return teach_program
        else:
            raise HTTPException(status_code=400, detail=f"Записи с таким id не существует")
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Ошибка получения записи: {err}")
    except HTTPException as err:
        raise err
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"ERROR: {err}")