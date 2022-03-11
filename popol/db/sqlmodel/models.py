from datetime import datetime

try:
    from humps.main import depascalize
    from sqlalchemy import Column, DateTime
    from sqlalchemy.orm.decl_api import declared_attr
    from sqlmodel import Field, SQLModel

except ImportError:
    raise RuntimeError(
        "SQLModel is not installed. Please install it with `pip install sqlmodel pyhumps`"
    )


class Model(SQLModel):
    id: int = Field(primary_key=True)
    date_created: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    date_updated: datetime = Field(sa_column=Column(DateTime, onupdate=datetime.utcnow))

    @declared_attr
    def __tablename__(cls):
        """
        Convert Pascal class name style to `snake_case`
        """
        return depascalize(cls.__name__)
