import scrapy

from ..items import NewsItem
from ..loaders import NewsLoader


class TWPSpider(scrapy.Spider):
    name = "thewashingtonpost"
    db_name = "The Washington Post"
    start_urls = [
        "https://www.washingtonpost.com/world/",
    ]

    def parse(self, response, **kwargs):
        for article in response.css("main article div div.w-100.grid"):
            relative_url = article.css("a.hover-blue::attr(href)").get()
            absolute_url = response.urljoin(relative_url)

            kws = {
                "title": article.css("a.hover-blue h3::text").get(),
                "source_name": self.db_name,
                "source_unique_id": relative_url.split("/")[-2],
                "url": absolute_url,
                "img_url": article.css("figure div img::attr(src)").get(),
                "description": article.css("p::text").get(),
            }

            item = NewsLoader(item=NewsItem(**kws), response=response)

            yield item.load_item()
