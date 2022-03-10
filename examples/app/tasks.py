from app.core import goodreads


async def scrape_quote(ctx: dict, *, tag: str):
    """
    Scrapes a quote from the internet.
    """

    print("Scraping quote...")
    app = ctx["app"]
    cache = app.state.cache
    quotes = await goodreads.get_quotes(tag)
    cache.set(tag, quotes, 60)
    print("Done")
