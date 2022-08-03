from popol.cache.globals import cache
from popol.db.sqlmodel.globals import db

from app.core import goodreads
from app.models import Counter


async def scrape_quote(ctx: dict, *, tag: str):
    """
    Scrapes a quote from the internet.
    """

    print("Scraping quote...")
    quotes = await goodreads.get_quotes(tag)
    cache.set(tag, quotes, 120)
    print("Done")


async def counter(ctx: dict):
    """
    Increments the counter.
    """

    with db.open() as session:
        counter: Counter = session.query(Counter).first()
        if not counter:
            counter = Counter(value=1)
            session.add(counter)
            session.commit()
            session.refresh(counter)
        counter.value += 1
        session.add(counter)
        session.commit()
        print("Counter value:", counter.value)
