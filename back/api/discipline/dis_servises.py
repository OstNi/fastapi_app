from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.discipline.dis_models import ShowDiscipline
from api.discipline.dis_models import CreateDiscipline
from api.discipline.dis_dals import DisciplineDAL

from data_base.db_models import Discipline


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


async def _get_all_discipline(session: AsyncSession) -> List[Discipline] | None:
    async with session.begin():
        dis_dal = DisciplineDAL(session)
        disciplines = await dis_dal.get_all_discipline()
        if disciplines is not None:
            return disciplines


async def _delete_discipline(dis_id, session: AsyncSession) -> ShowDiscipline | None:
    async with session.begin():
        dis_dal = DisciplineDAL(session)
        discipline: ShowDiscipline = await dis_dal.delete_discipline(dis_id)
        if discipline is not None:
            return discipline
