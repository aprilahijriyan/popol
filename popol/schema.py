from typing import Generic, List, Optional, TypeVar

from pydantic import __version__ as PYDANTIC_VERSION, BaseModel

if not PYDANTIC_VERSION.startswith("2"):
    from pydantic.generics import GenericModel
else:
    # pydantic >= 2.0
    GenericModel = BaseModel

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
