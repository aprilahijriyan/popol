from fastapi import APIRouter, Request
from popol.cache.globals import cache
from popol.jobs.saq.globals import saq_queue
from popol.schema import Page

from app.core import goodreads
from app.core.goodreads import Quote
from app.core.pagination import get_paginated_response
from app.schema import DetailSchema


class QuoteCreateOut(DetailSchema):
    job_id: str


router = APIRouter(prefix="/goodreads", tags=["Goodreads"])


@router.get("/quotes/{tag}", summary="Get quotes by tag", response_model=Page[Quote])
async def get_quotes(request: Request, tag: str, page: int = 1, page_size: int = 10):
    """
    Get quotes from the goodreads.com.
    """

    quotes = cache.get(tag)
    if not quotes:
        quotes = await goodreads.get_quotes(tag)
        cache.set(tag, quotes, 15)

    return get_paginated_response(quotes, page, page_size)


@router.post(
    "/quotes/{tag}",
    summary="Create a job to get quotes by tag",
    response_model=QuoteCreateOut,
)
async def create_job(request: Request, tag: str):
    """
    Create a job to get quotes by tag.
    """

    job = await saq_queue.enqueue("scrape_quote", tag=tag)
    return {"detail": "Job created", "job_id": job.id}
