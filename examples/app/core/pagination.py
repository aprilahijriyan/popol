from typing import TypeVar

from popol.db.sqlmodel.models import Model
from popol.pagination import PageNumberPagination
from sqlalchemy.orm.query import Query

T = TypeVar("T")


class Pagination(PageNumberPagination):
    def paginate(self, data: T) -> list:
        offset = self.get_offset()
        limit = self.get_limit()
        if isinstance(data, Query):
            data = data.offset(offset).limit(limit).all()

        results = []
        for d in data:
            if isinstance(d, Model):
                d = d.dict()
            results.append(d)
        return results

    def get_total_data(self, data: T) -> int:
        if isinstance(data, Query):
            rv = data.count()
        else:
            rv = len(data)
        return rv


def get_paginated_response(data: T, page: int, page_size: int) -> dict:
    p = Pagination(page, page_size)
    return p.get_paginated_response(data)
