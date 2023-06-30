"""Файл с настроиками и конфигурациями проекта"""

from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5450/postgres"
)  # путь соединения с бд
