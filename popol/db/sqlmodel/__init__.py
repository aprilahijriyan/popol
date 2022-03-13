from typing import Union

from fastapi import FastAPI
from pydantic import BaseSettings

from ...utils import get_settings

try:
    from sqlalchemy.engine import Engine
    from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
    from sqlmodel import Session, SQLModel, create_engine
    from sqlmodel.ext.asyncio.session import AsyncSession

except ImportError:
    raise RuntimeError(
        "SQLModel is not installed. Please install it with `pip install sqlmodel pyhumps`"
    )


class Database:
    """
    A class to wrap the sqlalchemy engine and open a connection session to the db.
    """

    def __init__(self, engine: Union[Engine, AsyncEngine], is_async: bool = False):
        self.engine = engine
        self.is_async = is_async

    def open(self) -> Union[Session, AsyncSession]:
        if self.is_async:
            return AsyncSession(self.engine)
        else:
            return Session(self.engine)


def setup(app: FastAPI, settings: BaseSettings = None) -> Database:
    """
    Install the sqlmodel plugin to the app.
    This will attach 1 attribute to `app.state` i.e:

    * `db` - `popol.sqlmodel.Database` instance object to open db connection.

    Args:
        app: FastAPI app.
        settings: The settings (can be pydantic.BaseSettings).

    Returns:
        Database: The database.
    """

    settings = get_settings(app, settings)
    prefix = "SQLALCHEMY_"
    db_uri = getattr(settings, f"{prefix}DATABASE_URI", None)
    if not db_uri:
        raise RuntimeError(f"{prefix}DATABASE_URI is not set")

    async_mode = getattr(settings, f"{prefix}ASYNC_MODE", False)
    options = getattr(settings, f"{prefix}OPTIONS", {})
    if async_mode:
        engine = create_async_engine(db_uri, **options)
    else:
        engine = create_engine(db_uri, **options)

    db = Database(engine, async_mode)
    app.state.db = db

    async def startup():
        # reference: https://github.com/tiangolo/sqlmodel/issues/54#issue-981884262
        if async_mode:
            async with engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
        else:
            SQLModel.metadata.create_all(engine)

    app.add_event_handler("startup", startup)
    return db
