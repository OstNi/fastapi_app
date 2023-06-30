from typing import List

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.db_models import Discipline


class DisciplineDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_discipline(self, name: str) -> Discipline:
        new_discipline = Discipline(name=name)
        self.db_session.add(new_discipline)
        await self.db_session.flush()
        return new_discipline

    async def get_all_discipline(self) -> List[Discipline] | None:
        query = select(Discipline)
        res = await self.db_session.execute(query)
        discipline_list = res.scalars().all()
        if discipline_list is not None:
            return discipline_list

    async def update_discipline(self, dis_id, **kwargs) -> Discipline | None:
        query = (
            update(Discipline)
            .where(Discipline.dis_id == dis_id)
            .values(kwargs)
            .returning(Discipline.dis_id)
        )

        res = await self.db_session.execute(query)
        update_dis_id_row = res.fetchone()
        if update_dis_id_row is not None:
            return update_dis_id_row[0]

    async def delete_discipline(self, dis_id) -> Discipline | None:
        query = (
            select(Discipline)
            .where(Discipline.dis_id == dis_id)
        )

        res = await self.db_session.execute(query)
        discipline = res.fetchone()
        if discipline:
            await self.db_session.delete(discipline)
            await self.db_session.commit()
            return discipline
