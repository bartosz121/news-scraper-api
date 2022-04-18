import scrapy

from ..items import NewsItem
from ..loaders import NewsLoader


class BBCSpider(scrapy.Spider):
    name = "bbc"
    db_name = "BBC"
    start_urls = [
        "https://www.bbc.com/news/world/",
    ]

    def parse(self, response, **kwargs):
        for article in response.css("div#index-page").css("div.gs-c-promo"):
            relative_url = article.css("a.gs-c-promo-heading::attr(href)").get()
            absolute_url = response.urljoin(relative_url)

            kws = {
                "title": article.css("h3.gs-c-promo-heading__title::text").get(),
                "source_name": self.db_name,
                "source_unique_id": article.css("a.gs-c-promo-heading::attr(href)").re(
                    r"(\d*$)"
                )[0],
                "url": absolute_url,
                "img_url": article.css(
                    "div.gs-o-media-island img::attr(data-src)"
                ).get(),
                "description": article.css("p.gs-c-promo-summary::text").get(),
            }

            item = NewsLoader(item=NewsItem(**kws), response=response)

            yield item.load_item()
