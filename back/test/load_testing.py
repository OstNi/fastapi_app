from api.dis_handlers import create_discipline
from back.api.discipline import update_discipline
from back.schemas.discipline import UpdateDiscipline
from back.schemas.discipline import CreateDiscipline
import uuid

import time


def timer_and_output(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time

            with open(filename, 'a') as file:
                file.write(f"Функция {func.__name__} выполнилась за {execution_time} секунд.\n")

            return result
        return wrapper
    return decorator


@timer_and_output("create_test.txt")
def create() -> int:
    st_idx = 0
    for i in range(100_000):
        res = create_discipline(
            CreateDiscipline(
                name=str(uuid.uuid4())
            )
        )
        if i == 0:
            st_idx = res.dis_id

    return st_idx


@timer_and_output("update_test.txt")
def update(st_idx):
    for i in range(st_idx, st_idx+100_000):
        update_discipline(
            dis_id=i,
            body=UpdateDiscipline(
                name=str(uuid.uuid4())
            )
        )


def main():
    st_idx = create()
    update(st_idx)