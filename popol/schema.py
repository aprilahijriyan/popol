from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

GenericResultsType = TypeVar("GenericResultsType")


class PagingField(BaseModel):
    next: Optional[int]
    prev: Optional[int]
    pages: List[int]


class Page(GenericModel, Generic[GenericResultsType]):
    total: int
    rows: int
    paging: PagingField
    data: List[GenericResultsType]
