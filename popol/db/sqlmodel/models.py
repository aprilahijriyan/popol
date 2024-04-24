from datetime import datetime, timezone
from typing import Optional

try:
    from humps.main import depascalize
    from sqlalchemy.orm.decl_api import declared_attr
    from sqlmodel import Field, SQLModel

except ImportError:
    raise RuntimeError(
        "SQLModel is not installed. Please install it with `pip install sqlmodel pyhumps`"
    )


class Model(SQLModel):
    """
    Abstract model providing `id`, `date_created` and `date_updated` fields.
    And also automatic table naming to `snake_case`.
    """

    id: int = Field(primary_key=True)
    date_created: datetime = Field(sa_column_kwargs={"default": datetime.now(timezone.utc)})
    date_updated: Optional[datetime] = Field(
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc), "nullable": True}
    )

    @declared_attr
    def __tablename__(cls):
        """
        Convert Pascal class name style to `snake_case`
        """
        return depascalize(cls.__name__)
