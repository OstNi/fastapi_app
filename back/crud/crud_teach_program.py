import asyncio
from typing import Any, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase

from data_base.db_models import TeachProgram
from data_base.db_models import Discipline
from data_base.db_models import TeachProgType
from schemas import CreateTeachProgram, UpdateTeachProgram


class CrudTeachProgram(CRUDBase[TeachProgram, CreateTeachProgram, UpdateTeachProgram]):

    async def get_multi(
            self, db: AsyncSession,
            *,
            skip: int | None = None,
            limit: int | None = None
    ) -> Sequence[Row | RowMapping | Any]:
        query = select(self.model).join(Discipline).join(TeachProgType)

        if skip is not None:
            query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)

        data = await db.execute(query)

        return data.scalars().all()


teach_program = CrudTeachProgram(TeachProgram, "tpr_id")

__all__ = [teach_program]