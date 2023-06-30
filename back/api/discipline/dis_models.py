from ..base_model import PydanticBaseModel

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import validator
from pydantic import constr
import re


# только буквы
LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


"""Pydantic models"""


class ShowDiscipline(PydanticBaseModel):
    dis_id: int
    name: str
    #
    # def __repr__(self):
    #     return f"PYDANTIC dis_id: {self.dis_id}, name: {self.name}"


class CreateDiscipline(BaseModel):
    name: constr(max_length=500)

    @validator("name")
    def valid_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Имя должно состоять только из букв"
            )
        return value


class DeleteDisciplineResponse(BaseModel):
    dis_id: int


class UpdateDisciplineResponse(BaseModel):
    dis_id: int


class UpdateDisciplineRequest(BaseModel):
    name: constr(max_length=500)

    @validator("name")
    def valid_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Имя должно состоять только из букв"
            )
        return value


