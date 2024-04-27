from popol.db.sqlmodel import models
from enum import Enum

class Counter(models.Model, table=True):
    value: int

class Hero(models.Model, table=True):
    class Roles(str, Enum):
        ROAM = "ROAM"
        EXPLANE = "EXPLANE"
        MIDLANE = "MIDLANE"
        GOLDLANE = "GOLDLANE"
        JUNGLER = "JUNGLER"

    name: str
    role: Roles
