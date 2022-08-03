from popol.db.sqlmodel import models
from sqlmodel import Field


class Account(models.Model, table=True):
    class Config:
        orm_mode = True

    username: str = Field(max_length=255, nullable=False)
    password: str = Field(max_length=255, nullable=False)


class Counter(models.Model, table=True):
    value: int
