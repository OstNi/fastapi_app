from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.discipline.dis_models import ShowDiscipline
from api.discipline.dis_models import CreateDiscipline
from api.discipline.dis_dals import DisciplineDAL

from data_base.db_models import Discipline


from sqlalchemy.ext.asyncio import AsyncSession
from data_base.session import get_db
from fastapi import Depends


async def _create_new_discipline(body: CreateDiscipline, session: AsyncSession) -> ShowDiscipline:
    async with session.begin():
        dis_dal = DisciplineDAL(session)
        discipline = await dis_dal.create_discipline(
            name=body.name
        )

        return ShowDiscipline(
            dis_id=discipline.dis_id,
            name=discipline.name
        )


async def _get_all_discipline(session: AsyncSession) -> List[ShowDiscipline] | None:
    async with session.begin():
        dis_dal = DisciplineDAL(session)
        discipline_list = await dis_dal.get_all_discipline()
        if discipline_list is not None:
            return [ShowDiscipline(dis_id=discipline.dis_id, name=discipline.name) for discipline in discipline_list]


async def _delete_discipline(dis_id: int, session: AsyncSession) -> ShowDiscipline | None:
    async with session.begin():
        dis_dal = DisciplineDAL(session)
        deleted_discipline = await dis_dal.delete_discipline(dis_id)
        if deleted_discipline is not None:
            return ShowDiscipline(
                dis_id=deleted_discipline.dis_id,
                name=deleted_discipline.name
            )


async def _update_discipline(dis_id: int, session: AsyncSession, **kwargs) -> ShowDiscipline | None:
    async with session.begin():
        dis_dal = DisciplineDAL(session)
        updated_discipline = await dis_dal.update_discipline(dis_id, **kwargs)
        if updated_discipline is not None:
            return ShowDiscipline(
                dis_id=updated_discipline.dis_id,
                name=updated_discipline.name
            )