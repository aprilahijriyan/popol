from abc import ABCMeta, abstractmethod
from typing import List, Sequence, TypeVar

T = TypeVar("T")


class Pagination(metaclass=ABCMeta):
    """
    Abstract class for pagination
    """

    def __init__(self, *args, **kwds) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def paginate(self, data: T) -> Sequence:
        pass  # pragma: no cover

    @abstractmethod
    def get_paginated_response(self, data: T) -> dict:
        pass


class PageNumberPagination(Pagination):
    """
    Pagination class for page number
    """

    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

    def get_offset(self) -> int:
        return self.page_size * (self.page - 1)

    def get_limit(self) -> int:
        return self.page_size

    def paginate(self, data: Sequence) -> Sequence:
        offset = self.get_offset()
        limit = self.get_limit()
        return data[offset : offset + limit]

    def get_total_data(self, data: T) -> int:
        """
        Get total data.
        Might be useful if the data is a QuerySet or something that can compute :)
        """

        return len(data)

    def get_total_page(self, total: int, page_size: int = 10) -> List[int]:
        """
        Get total pages.
        Args:
            total: Total data.
            page_size: Page size.
        """

        if total == 0:
            return [1]  # pragma: no cover

        return list(
            range(
                1,
                (
                    total // page_size + 1
                    if total % page_size != 0
                    else total // page_size
                )
                + 1,
            )
        )

    def get_paginated_response(
        self,
        data: T,
    ) -> dict:
        """
        Return a paginated response.
        Args:
            data: Data to be paginated.
        """

        # Counting all pages
        total_data = self.get_total_data(data)
        pages = self.get_total_page(total_data, self.page_size)
        prev_page = self.page - 1
        if prev_page not in pages:
            prev_page = None  # type: ignore[assignment]

        next_page = self.page + 1
        if next_page not in pages:
            next_page = None  # type: ignore[assignment]

        # Get data per page
        data = self.paginate(data)
        rows = self.get_total_data(data)
        result = {
            "total": total_data,
            "rows": rows,
            "paging": {"next": next_page, "prev": prev_page, "pages": pages},
            "data": data,
        }
        return result
