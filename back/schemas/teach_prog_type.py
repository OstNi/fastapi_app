from schemas.base_model import PydanticBaseModel

from pydantic import BaseModel
from pydantic import constr


class SowTeachProgType(PydanticBaseModel):
    tpt_id: int
    tp_type: constr(max_length=255)
    type_info: constr(max_length=240) | None = None


class CreateTeachProgType(BaseModel):
    tp_type: constr(max_length=255)
    type_info: constr(max_length=240) | None = None


class UpdateTeachProgType(BaseModel):
    tp_type: constr(max_length=255) | None = None
    type_info: constr(max_length=240) | None = None
