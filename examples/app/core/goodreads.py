from pprint import pprint
from typing import List, TypedDict

import anyio
from bs4 import BeautifulSoup
from bs4.element import Tag
from httpx import AsyncClient


class Quote(TypedDict):
    """
    A quote from the goodreads.com.
    """

    author: str
    text: str
    likes: str
    tags: List[str]


def parse_quote(quote: Tag) -> Quote:
    """
    Parse a quote from the goodreads.com.
    """

    quote_text_tag = quote.select_one("div.quoteText")
    author_tag = quote_text_tag.select_one("span.authorOrTitle")
    author = author_tag.text.strip().rstrip(",")
    author_tag.decompose()
    quote_text = ""
    for text in quote_text_tag.text.strip().splitlines():
        quote_text += text.strip()

    text = ""
    for part in quote_text.split("."):
        text += part.strip() + ". "

    text = text.replace("“", "").replace("”", "")
    if "―" in text:
        text = text.split("―")[0].strip()

    quote_footer = quote.select_one("div.quoteFooter")
    quote_tags = quote_footer.select("div:nth-child(1) > a")
    tags = [tag.text.strip() for tag in quote_tags]
    quote_likes = quote_footer.select_one("div:nth-child(2) > a").text.strip()
    return {"author": author, "text": text, "likes": quote_likes, "tags": tags}


async def get_quotes(tag: str) -> List[Quote]:
    """
    Get quotes from the goodreads.com.
    """

    url = f"https://www.goodreads.com/quotes/tag?utf8=%E2%9C%93&id={tag}"
    quotes = []
    async with AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        quote_tags = soup.select("div.leftContainer > div.quote")
        for quote_tag in quote_tags:
            quote = parse_quote(quote_tag)
            quotes.append(quote)

    return quotes


async def main():
    quotes = await get_quotes("love")
    for quote in quotes:
        pprint(quote)


if __name__ == "__main__":
    anyio.run(main)
