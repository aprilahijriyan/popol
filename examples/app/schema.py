from pydantic import BaseModel


class DetailSchema(BaseModel):
    detail: str
