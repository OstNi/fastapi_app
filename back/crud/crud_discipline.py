from crud.base import CRUDBase

from data_base.db_models import Discipline

from schemas.discipline import CreateDiscipline
from schemas.discipline import UpdateDiscipline


class CrudDiscipline(CRUDBase[Discipline, CreateDiscipline, UpdateDiscipline]):
    pass


discipline = CrudDiscipline(Discipline, "dis_id")

__all__ = [discipline]
