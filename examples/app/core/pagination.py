from typing import Sequence

from popol.pagination import PageNumberPagination


def get_paginated_response(data: Sequence, page: int, page_size: int) -> dict:
    p = PageNumberPagination(page, page_size)
    return p.get_paginated_response(data)
