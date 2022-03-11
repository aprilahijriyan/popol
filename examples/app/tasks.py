from popol.cache.backends.redis import RedisBackend
from popol.db.sqlmodel import Database

from app.core import goodreads
from app.models import Counter


async def scrape_quote(ctx: dict, *, tag: str):
    """
    Scrapes a quote from the internet.
    """

    print("Scraping quote...")
    app = ctx["app"]
    cache: RedisBackend = app.state.cache
    quotes = await goodreads.get_quotes(tag)
    cache.set(tag, quotes, 60)
    print("Done")


async def counter(ctx: dict):
    """
    Increments the counter.
    """

    print("Incrementing counter...")
    app = ctx["app"]
    db: Database = app.state.db
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
    print("Done")
