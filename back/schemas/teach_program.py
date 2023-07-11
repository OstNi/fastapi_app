from schemas.base_model import PydanticBaseModel

from pydantic import BaseModel
from pydantic import constr
from pydantic import PastDate

from .discipline import ShowDiscipline
from .teach_prog_type import SowTeachProgType


class ShowTeachProgram(PydanticBaseModel):
    tpr_id: int
    confirm_date: PastDate | None = None
    status: constr(max_length=1)
    protocol: constr(max_length=255) | None = None
    practice_form: constr(max_length=255) | None = None
    practice_schedule: constr(max_length=255) | None = None
    info: constr(max_length=4000) | None = None
    dis_dis_id: int
    tpt_tpt_id: int
    dis_dis: ShowDiscipline
    tpt_tpt: SowTeachProgType


class CreateTeachProgram(BaseModel):
    confirm_date: PastDate | None = None
    status: constr(max_length=1)
    protocol: constr(max_length=255) | None = None
    practice_form: constr(max_length=255) | None = None
    practice_schedule: constr(max_length=255) | None = None
    info: constr(max_length=4000) | None = None
    dis_dis_id: int
    tpt_tpt_id: int


class UpdateTeachProgram(BaseModel):
    confirm_date: PastDate | None = None
    status: constr(max_length=1) | None = None
    protocol: constr(max_length=255) | None = None
    practice_form: constr(max_length=255) | None = None
    practice_schedule: constr(max_length=255) | None = None
    info: constr(max_length=4000) | None = None
    dis_dis_id: int | None = None
    tpt_tpt_id: int | None = None
