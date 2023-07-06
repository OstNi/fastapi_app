from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Sequence

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Row, RowMapping
from sqlalchemy import exc
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from pydantic import BaseModel

from data_base.db_models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def exc_raiser(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc.IntegrityError as err:
            raise err
        except Exception as err:
            raise err

    return wrapper


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], id: str):
        self.id = id
        self.model = model

    @exc_raiser
    async def get(self, db: AsyncSession, *, obj_id: Any) -> Optional[ModelType]:
        query = select(self.model).filter(getattr(self.model, self.id) == obj_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @exc_raiser
    async def get_multi(
            self, db: AsyncSession,
            *,
            skip: int | None = None,
            limit: int | None = None
    ) -> Sequence[Row | RowMapping | Any]:
        query = select(self.model)

        if skip is not None:
            query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)

        data = await db.execute(query)

        return data.scalars().all()

    @exc_raiser
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @exc_raiser
    async def update(
            self,
            db: AsyncSession,
            *,
            obj_id: int,
            obj_in: UpdateSchemaType | Dict[str, Any],
    ) -> int:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        try:
            query = (
                sqlalchemy_update(self.model)
                .where(getattr(self.model, self.id) == obj_id)
                .values(**update_data)
            )

            async with db.begin():
                res = await db.execute(query)
                return res.rowcount

        except Exception as err:
            raise err

    @exc_raiser
    async def remove(self, db: AsyncSession, *, obj_id: int) -> dict:
        query = sqlalchemy_delete(self.model).where(getattr(self.model, self.id) == obj_id)
        try:
            async with db.begin():
                result = await db.execute(query)
                return result.rowcount
        except Exception as err:
            await db.rollback()
            raise err
