import scrapy

from ..items import NewsItem
from ..loaders import NewsLoader


class TheEconomistSpider(scrapy.Spider):
    name = "theeconomist"
    db_name = "The Economist"
    start_urls = [
        "https://www.economist.com/weeklyedition/",
    ]

    def parse(self, response, **kwargs):
        for article in response.css(
            "section.layout-weekly-edition-section div.teaser-weekly-edition--leaders"
        ):
            relative_url = article.css("a.headline-link::attr(href)").get()
            absolute_url = response.urljoin(relative_url)

            kws = {
                "title": article.css(
                    "a.headline-link span.teaser__headline::text"
                ).get(),
                "source_name": self.db_name,
                "source_unique_id": relative_url.split("/")[-1],
                "url": absolute_url,
                "img_url": article.css("div.teaser__image img::attr(src)").get(),
                "description": article.css("p.teaser__description::text").get(),
            }

            item = NewsLoader(item=NewsItem(**kws), response=response)

            yield item.load_item()
