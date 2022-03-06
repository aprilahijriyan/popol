from fastapi import APIRouter, Request
from popol.cache.backends.redis import RedisBackend

from app.core import goodreads
from app.core.pagination import get_paginated_response

router = APIRouter(prefix="/goodreads", tags=["Goodreads"])


@router.get("/quotes/{tag}", summary="Get quotes by tag")
async def get_quotes(request: Request, tag: str, page: int = 1, page_size: int = 10):
    """
    Get quotes from the goodreads.com.
    """

    cache: RedisBackend = request.app.state.cache
    quotes = cache.get(tag)
    if not quotes:
        quotes = await goodreads.get_quotes(tag)
        cache.set(tag, quotes, 15)

    return get_paginated_response(quotes, page, page_size)
