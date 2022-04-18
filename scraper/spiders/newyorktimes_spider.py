import scrapy

from ..items import NewsItem
from ..loaders import NewsLoader


class NewYorkTimesSpider(scrapy.Spider):
    name = "newyorktimes"
    db_name = "New York Times"
    start_urls = [
        "https://www.nytimes.com/section/world/",
    ]

    def parse(self, response, **kwargs):
        for article in response.css("section#collection-highlights-container div").css(
            "article"
        ):
            relative_url = article.css("h2 a::attr(href)").get()
            absolute_url = response.urljoin(relative_url)
            source_unique_id = relative_url.split("/")[-1].rstrip(".html")

            kws = {
                "title": article.css("h2 a::text").get(),
                "source_name": self.db_name,
                "source_unique_id": source_unique_id,
                "url": absolute_url,
                "img_url": article.css("figure img::attr(src)").get(),
                "description": article.css("p::text").get(),
            }

            item = NewsLoader(item=NewsItem(**kws), response=response)

            yield item.load_item()
