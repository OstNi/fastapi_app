from schemas.base_model import PydanticBaseModel

from pydantic import BaseModel
from pydantic import constr


"""Pydantic models"""


class ShowDiscipline(PydanticBaseModel):
    dis_id: int
    name: str


class CreateDiscipline(BaseModel):
    name: constr(max_length=500)


class UpdateDiscipline(BaseModel):
    name: constr(max_length=500)


